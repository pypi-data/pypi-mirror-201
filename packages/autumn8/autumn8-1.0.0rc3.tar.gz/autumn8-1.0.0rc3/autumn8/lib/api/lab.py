import io
import json
import os
import urllib
import urllib.parse
from http import HTTPStatus
from threading import Lock
from typing import Dict, List

import appdirs
import requests
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import PartTypeDef
from requests.auth import HTTPBasicAuth
from tqdm.contrib.concurrent import thread_map

from autumn8.cli import pending_uploads
from autumn8.cli.analyze import filepath_is_a_link
from autumn8.cli.cli_environment import CliEnvironment
from autumn8.common.config.s3 import init_s3, init_s3_client, s3path_join
from autumn8.lib import logging
from autumn8.lib.api_creds import retrieve_api_creds

DEFAULT_MAX_UPLOAD_WORKERS = 4

APP_NAME = "autumn8"
APP_AUTHOR = "autumn8"

logger = logging.getLogger(__name__)

data_dir = appdirs.user_data_dir(APP_NAME, APP_AUTHOR)


def url_with_params(url, params):
    url_parse = urllib.parse.urlparse(url)
    url_new_query = urllib.parse.urlencode(params)
    url_parse = url_parse._replace(query=url_new_query)

    new_url = urllib.parse.urlunparse(url_parse)
    return new_url


def require_ok_response(response):
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise Exception(
            f"Received response {response.status_code}:\n{response.text}\n\nUser not authenticated; please run `autumn8-cli login` to authorize your CLI"
        )
    if response.status_code != HTTPStatus.OK:
        raise Exception(
            f"Received response {response.status_code}:\n{response.text}"
        )


def fetch_user_data(environment: CliEnvironment):
    user_id, api_key = None, None
    autodl_host = environment.value.app_host
    try:
        user_id, api_key = retrieve_api_creds()
    except:
        raise Exception(
            f"API key is missing! To configure API access, please visit {autodl_host}/profile and generate an API key, then run `autumn8-cli login`"
        )

    user_api_route = f"{autodl_host}/api/user"
    response = requests.get(
        user_api_route,
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth(user_id, api_key),
    )

    require_ok_response(response)
    return json.loads(response.text)["user"]


def post_model(environment: CliEnvironment, organization_id, model_config):
    autodl_host = environment.value.app_host
    api_route = f"{autodl_host}/api/lab/model"
    logger.info("Submitting model to %s", api_route)
    response = requests.post(
        url_with_params(api_route, {"organization_id": organization_id}),
        headers={"Content-Type": "application/json"},
        data=json.dumps(model_config),
        auth=HTTPBasicAuth(*retrieve_api_creds()),
    )

    require_ok_response(response)
    return response.json()


def delete_model(environment: CliEnvironment, organization_id, model_id):
    autodl_host = environment.value.app_host
    new_url = url_with_params(
        f"{autodl_host}/api/lab/model",
        {"model_id": model_id, "organization_id": organization_id},
    )
    response = requests.delete(
        new_url,
        auth=HTTPBasicAuth(*retrieve_api_creds()),
    )
    require_ok_response(response)


def normal_or_multipart_upload(
    environment,
    s3_file_url,
    f,
    resume_args,
    id_key,
    mpu_id=None,
    max_upload_workers=DEFAULT_MAX_UPLOAD_WORKERS,
):
    f.seek(0, 2)  # seek to end of file
    total_bytes = f.tell()
    f.seek(0)
    # AWS dissallow multipart upload of files under 5MB
    if total_bytes < 6 * 1024**2:
        normal_upload(environment, s3_file_url, f)
    else:
        multipart_upload(
            environment=environment,
            s3_file_url=s3_file_url,
            file=f,
            resume_args=resume_args,
            id_key=id_key,
            mpu_id=mpu_id,
            max_upload_workers=max_upload_workers,
        )


def normal_upload(environment: CliEnvironment, s3_file_url, f):
    S3 = init_s3(environment.value.s3_host)

    compatible_s3_file_url = get_hacked_legacy_backwards_compatible_s3_file_url(
        environment.value.s3_bucket_root_folder, s3_file_url
    )

    S3.Bucket(environment.value.s3_bucket_name).Object(
        compatible_s3_file_url
    ).upload_fileobj(f)


def get_uploaded_parts(
    s3_client: S3Client, s3_bucket_name, s3_file_url, upload_id
) -> List[PartTypeDef]:
    res = s3_client.list_parts(
        Bucket=s3_bucket_name, Key=s3_file_url, UploadId=upload_id
    )
    return list(res["Parts"]) if "Parts" in res else []


def upload_part(
    part_number,
    s3_client: S3Client,
    s3_bucket_name,
    s3_file_url,
    file,
    part_size_in_bytes,
    total_bytes,
    mpu_id,
    parts_already_uploaded: Dict[int, PartTypeDef],
    lock,
):
    with lock:
        file.seek((part_number - 1) * part_size_in_bytes)
        data = file.read(part_size_in_bytes)

    if not len(data):
        return

    if part_number in parts_already_uploaded:
        part = parts_already_uploaded[part_number]
        # FIXME: these checks are pretty slow, I'm not sure why
        if len(data) != part.get("Size"):
            raise Exception(
                "Upload corrupted: Size mismatch: local "
                + str(len(data))
                + ", remote: "
                + str(part.get("Size"))
            )
        return
    else:
        part = s3_client.upload_part(
            Body=data,
            Bucket=s3_bucket_name,
            Key=s3_file_url,
            UploadId=mpu_id,
            PartNumber=part_number,
        )


def multipart_upload(
    environment: CliEnvironment,
    s3_file_url,
    file,
    resume_args,
    id_key,
    mpu_id=None,
    max_upload_workers=DEFAULT_MAX_UPLOAD_WORKERS,
):
    file.seek(0, 2)  # seek to end of file
    total_bytes = file.tell()
    file.seek(0)  # seek to start of file
    # max total upload size is 100GB
    part_size_in_bytes = max(
        10 * 1024**2, total_bytes // 500
    )  # minimum part size on aws is 5MB, list part returns max 1000 parts

    # we have to use low-level API to be able to support
    # resumable uploads - https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-upload-object.html
    s3_client = init_s3_client(environment.value.s3_host)
    s3_bucket_name = environment.value.s3_bucket_name

    compatible_s3_file_url = get_hacked_legacy_backwards_compatible_s3_file_url(
        environment.value.s3_bucket_root_folder, s3_file_url
    )

    if mpu_id != None:
        print(f"Resuming upload with id {mpu_id}")
        parts_already_uploaded = {
            part["PartNumber"]: part
            for part in get_uploaded_parts(
                s3_client, s3_bucket_name, compatible_s3_file_url, mpu_id
            )
            if "PartNumber" in part and "Size" in part
        }
    else:
        parts_already_uploaded = {}
        mpu = s3_client.create_multipart_upload(
            Bucket=s3_bucket_name, Key=compatible_s3_file_url
        )
        mpu_id = mpu["UploadId"]
        print(f"Created new multipart upload with id {mpu_id}")

    resume_args[id_key] = mpu_id
    pending_uploads.update_upload(resume_args["run_id"], resume_args)

    # +2, because we assume there's always this final part which is smaller than the rest, and the range end has to be larger by 1 because it's not included
    part_numbers_to_upload = set(
        range(1, (total_bytes - 1) // part_size_in_bytes + 2)
    )
    lock = Lock()
    thread_map(
        lambda part_number: upload_part(
            part_number=part_number,
            s3_client=s3_client,
            s3_bucket_name=s3_bucket_name,
            s3_file_url=compatible_s3_file_url,
            file=file,
            part_size_in_bytes=part_size_in_bytes,
            parts_already_uploaded=parts_already_uploaded,
            total_bytes=total_bytes,
            mpu_id=mpu_id,
            lock=lock,
        ),
        part_numbers_to_upload,
        max_workers=max_upload_workers,
    )

    all_parts = get_uploaded_parts(
        s3_client, s3_bucket_name, compatible_s3_file_url, mpu_id
    )

    s3_client.complete_multipart_upload(
        Bucket=s3_bucket_name,
        Key=compatible_s3_file_url,
        UploadId=mpu_id,
        MultipartUpload={
            "Parts": [  # type: ignore (partial Part type works fine in practice)
                {
                    "PartNumber": part.get("PartNumber"),
                    "ETag": part.get("ETag"),
                }
                for part in all_parts
            ]
        },
    )


# TODO: fix s3 file structure so that this is not needed
def get_hacked_legacy_backwards_compatible_s3_file_url(
    s3_root_folder_name,
    s3_file_url,
):
    return s3path_join(s3_root_folder_name, s3_file_url)


def post_model_file(
    environment: CliEnvironment,
    bytes_or_filepath,
    s3_file_url,
    resume_args,
    id_key,
    upload_id=None,
    max_upload_workers=DEFAULT_MAX_UPLOAD_WORKERS,
):
    if isinstance(bytes_or_filepath, io.BytesIO):
        f = bytes_or_filepath
        normal_or_multipart_upload(
            environment,
            s3_file_url,
            f,
            resume_args,
            id_key,
            upload_id,
            max_upload_workers=max_upload_workers,
        )
    else:
        if filepath_is_a_link(bytes_or_filepath):
            # attaching directly without any reuploads
            assert bytes_or_filepath == s3_file_url
            return

        with open(bytes_or_filepath, "rb") as f:
            normal_or_multipart_upload(
                environment,
                s3_file_url,
                f,
                resume_args,
                id_key,
                upload_id,
                max_upload_workers=max_upload_workers,
            )


def async_prediction(environment: CliEnvironment, organization_id, model_id):
    autodl_host = environment.value.app_host
    new_url = url_with_params(
        f"{autodl_host}/api/lab/model/async_prediction",
        {
            "model_id": model_id,
            "organization_id": organization_id,
        },
    )
    response = requests.post(
        new_url,
        auth=HTTPBasicAuth(*retrieve_api_creds()),
    )
    require_ok_response(response)
    return response

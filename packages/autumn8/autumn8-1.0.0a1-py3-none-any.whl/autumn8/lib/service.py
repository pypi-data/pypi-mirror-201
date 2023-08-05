import io
import os
import time
import uuid
from pathlib import Path
from typing import Optional

from autumn8.cli import pending_uploads
from autumn8.cli.cli_environment import CliEnvironment
from autumn8.common.config.s3 import get_global_anon_s3_resource, s3path_join
from autumn8.lib import api

DEFAULT_MAX_UPLOAD_WORKERS = 4


def resume_upload_model(upload_task):
    s3 = get_global_anon_s3_resource()

    try:
        return upload_model(**upload_task)
    except s3.meta.client.exceptions.NoSuchUpload:
        pending_uploads.abort_and_forget_upload(upload_task["run_id"])


def upload_model(
    environment: CliEnvironment,
    organization_id,
    model_config,
    model_file,
    input_file_path: Optional[str],
    max_upload_workers: int = DEFAULT_MAX_UPLOAD_WORKERS,
    model_file_upload_id: Optional[str] = None,
    input_file_upload_id: Optional[str] = None,
    run_id: Optional[str] = None,
    **kwargs,
):
    if run_id is None:  # used for resuming upload
        run_id = str(uuid.uuid4())
    if type(model_file) == io.BytesIO:
        model_file.seek(0)
        model_file_name = model_config["name"]  # TODO add extension?
    else:
        model_file_name = os.path.basename(model_file)

    s3_bucket_root_folder = environment.value.s3_bucket_root_folder

    model_type = None if "model_type" not in kwargs else kwargs["model_type"]

    s3_file_url = kwargs.get("s3_file_url") or generate_s3_file_url(
        organization_id=organization_id,
        run_id=run_id,
        model_file_name=model_file_name,
        s3_bucket_root_folder=s3_bucket_root_folder,
        model_type=model_type,
    )

    s3_input_file_url = None
    if input_file_path != None and len(input_file_path) > 0:
        filename = Path(input_file_path).name
        s3_input_file_url = kwargs.get(
            "s3_input_file_url"
        ) or generate_s3_input_file_url(
            organization_id=organization_id,
            run_id=run_id,
            s3_bucket_root_folder=s3_bucket_root_folder,
            filename=filename,
        )

    function_args = locals()

    time_start = time.time()
    print("Uploading the model files...")
    api.lab.post_model_file(
        environment,
        model_file,
        s3_file_url,
        function_args,
        "model_file_upload_id",
        model_file_upload_id,
        max_upload_workers=max_upload_workers,
    )
    model_config["s3_file_url"] = s3_file_url
    print("Model uploaded in", time.time() - time_start, "seconds")

    if s3_input_file_url is not None:
        time_start = time.time()
        print("Uploading the input files...")
        api.lab.post_model_file(
            environment,
            input_file_path,
            s3_input_file_url,
            function_args,
            "input_file_upload_id",
            input_file_upload_id,
            max_upload_workers=max_upload_workers,
        )
        model_config["s3_input_file_url"] = s3_input_file_url
        print("Inputs uploaded in", time.time() - time_start, "seconds")

    print("Creating the model entry in AutoDL...")
    model_id = api.lab.post_model(environment, organization_id, model_config)
    pending_uploads.forget_upload(run_id)

    autodl_host = environment.value.app_host

    print("Starting up performance predictor...")
    api.lab.async_prediction(environment, organization_id, model_id)
    return f"{autodl_host}/{organization_id}/performancePredictor/dashboard/{model_id}"


def generate_s3_input_file_url(
    organization_id, run_id, s3_bucket_root_folder, filename
):
    if s3_bucket_root_folder is None:
        s3_bucket_root_folder = ""

    return s3path_join(
        s3_bucket_root_folder,
        "inputs",
        f"{organization_id}-{run_id}-{filename}",
    )


def generate_s3_file_url(
    organization_id,
    run_id,
    model_file_name,
    s3_bucket_root_folder,
    model_type,
):
    additional_extension = f".{model_type}" if model_type is not None else ""
    if s3_bucket_root_folder is None:
        s3_bucket_root_folder = ""

    return s3path_join(
        s3_bucket_root_folder,
        "models",
        f"{organization_id}-{run_id}-{model_file_name}{additional_extension}",
    )

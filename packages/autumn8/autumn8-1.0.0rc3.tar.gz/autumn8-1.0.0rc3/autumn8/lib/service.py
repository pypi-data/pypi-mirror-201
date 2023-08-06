import io
import os
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

from autumn8.cli import pending_uploads
from autumn8.cli.analyze import filepath_is_a_link
from autumn8.cli.cli_environment import CliEnvironment
from autumn8.common.config.s3 import get_global_anon_s3_resource, s3path_join
from autumn8.lib import api, logging

DEFAULT_MAX_UPLOAD_WORKERS = 4

logger = logging.getLogger(__name__)


def resume_upload_model(upload_task):
    s3 = get_global_anon_s3_resource()

    try:
        return upload_model(**upload_task)
    except s3.meta.client.exceptions.NoSuchUpload:
        pending_uploads.abort_and_forget_upload(upload_task["run_id"])


def upload_model(
    environment: CliEnvironment,
    organization_id,
    model_config: Dict[str, Any],
    model_file: str,
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
        model_file=model_file,
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
    logger.info("Uploading the model files...")
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
    logger.debug("Model uploaded in %.03f seconds", time.time() - time_start)

    # TODO: support uploading inputs via links
    if s3_input_file_url is not None:
        time_start = time.time()
        logger.info("Uploading the input files...")
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
        logger.debug(
            "Inputs uploaded in %.03f seconds", time.time() - time_start
        )

    logger.info("Creating the model entry in AutoDL...")
    model_post_response = api.lab.post_model(
        environment, organization_id, model_config
    )
    model_id = model_post_response["id"]
    pending_uploads.forget_upload(run_id)

    logger.info("Starting up performance predictor...")
    api.lab.async_prediction(environment, organization_id, model_id)
    return model_post_response


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
    model_file,
    s3_bucket_root_folder,
    model_type,
):
    if filepath_is_a_link(model_file):
        return model_file

    additional_extension = f".{model_type}" if model_type is not None else ""
    if s3_bucket_root_folder is None:
        s3_bucket_root_folder = ""

    return s3path_join(
        s3_bucket_root_folder,
        "models",
        f"{organization_id}-{run_id}-{model_file_name}{additional_extension}",
    )

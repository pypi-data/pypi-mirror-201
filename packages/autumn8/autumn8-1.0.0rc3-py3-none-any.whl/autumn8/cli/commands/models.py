import enum
import json
import os
import random
import time
import uuid
import zipfile
from configparser import NoOptionError, NoSectionError
from typing import List, Optional

import click
import jsonschema
import questionary
from jsonschema import validate

from autumn8.cli import options
from autumn8.cli.analyze import analyze_model_file, suggest_model_name
from autumn8.cli.cli_environment import CliEnvironment
from autumn8.cli.examples import example_model_names
from autumn8.cli.interactive import announce_model_upload_response
from autumn8.common.config.settings import supported_quants
from autumn8.lib import api_creds, logging
from autumn8.lib import service as autodl
from autumn8.lib.api import lab

USER_ID_LENGTH = len(str(uuid.uuid4()))
API_KEY_LENGTH = 32

logger = logging.getLogger(__name__)


@click.group()
def model_commands_group():
    pass


@model_commands_group.command()
@options.use_environment
@options.use_quiet_mode
@click.option(
    "-u",
    "--user_id",
    "--user-id",
    help="The ID of the user that the CLI will authenticate as in AutoDL.",
)
@click.option(
    "-a",
    "--api_key",
    "--api-key",
    help="API Key to use when authenticating in AutoDL from now on.",
)
def login(user_id, api_key, environment: CliEnvironment, quiet):
    """Store API credentials for the CLI for future use."""

    logger.info(
        f"To setup up CLI access, please visit {environment.value.app_host}/profile - once you're signed in, generate a new API Key, then copy and paste the API Key data from the browser here\ngg"
    )
    try:
        old_user_id, _ = api_creds.retrieve_api_creds()
        if old_user_id not in ["", None]:
            logger.warning(
                f"Replacing existing credentials for the user with id={old_user_id}"
            )
    except (NoSectionError, NoOptionError):
        pass

    # using unsafe_ask so that the script is properly aborted on ^C
    # (instead of questionary passing `None` as the user's prompt answer)
    if user_id is None or len(user_id) != USER_ID_LENGTH:
        user_id = questionary.text(
            "User ID",
            validate=lambda user_id: len(user_id) == USER_ID_LENGTH,
        ).unsafe_ask()
    else:
        logger.info(f"User ID: {user_id}")
    if api_key is None or len(api_key) != API_KEY_LENGTH:
        api_key = questionary.text(
            "API Key",
            validate=lambda api_key: len(api_key) == API_KEY_LENGTH,
        ).unsafe_ask()
    else:
        logger.info(f"API Key: {api_key}")

    api_creds.store_api_creds(user_id, api_key)
    user_data = lab.fetch_user_data(environment)
    logger.info(f"Credentials set up successfully for {user_data['email']}!")


INPUT_DIMS_JSONSCHEMA = {
    "type": "array",
    "minItems": 1,
    "items": {
        "type": "array",
        "minItems": 1,
        "items": {"type": "number"},
    },
}


def validate_input_dims_json(jsonString):
    if jsonString == "":
        return True

    try:
        jsonData = json.loads(jsonString)
        validate(instance=jsonData, schema=INPUT_DIMS_JSONSCHEMA)
    except (
        jsonschema.exceptions.ValidationError,
        json.decoder.JSONDecodeError,
    ):
        return False
    return True


def validate_input_file(path):
    if not os.path.exists(path):
        return False

    if not os.path.isfile(path):
        return False

    try:
        with open(path, "r") as f:
            jsonData = json.load(f)

    except json.decoder.JSONDecodeError:
        return False
    return True


def normalize_input_dims_for_api(input_dims):
    if not input_dims:
        return None

    inputs = json.loads(input_dims)
    inputs = [[str(dim) for dim in input] for input in inputs]
    return json.dumps(inputs, separators=(",", ":"))


# cannot use click prompt kwargs feature for the command options, because we
# want to infer input dimensions and the model name
def prompt_for_missing_model_info(
    *,
    model_name: str,
    quantization,
    input_dims: Optional[str],
    input_file: Optional[str],
    inferred_model_name: str,
    inferred_quantization,
    inferred_input_dims: Optional[str],
    should_skip_inputs: bool,
    is_source_annotated_model=False,
):
    # TODO - attempt reading model details from some configCache files
    if model_name is None:
        model_name = questionary.text(
            f"Please give a name to your model to be used in AutoDL (for example: '{random.choice(example_model_names)}')\n  Model name:",
            validate=lambda name: len(name) > 0
            and len(name) <= 100
            and "/" not in name,
            default=inferred_model_name,
        ).unsafe_ask()
    if quantization is None:
        quantization = questionary.select(
            "Choose quantization for the model",
            choices=supported_quants,
            use_shortcuts=True,
            default=inferred_quantization,
        ).unsafe_ask()

    class INPUT_METHODS(enum.Enum):
        FILE = "Upload input file"
        SHAPE = "Specify input shape"
        INFER = "Let us try to infer input shape"

    input_method = INPUT_METHODS.INFER.value

    if input_file is not None and input_dims is not None:
        logger.warning("Cannot specify both input file and input dimensions")
        input_file = None
        input_dims = None

    if (
        input_dims is None
        and input_file is None
        and not is_source_annotated_model
        and not should_skip_inputs
    ):
        input_method = questionary.select(
            "Specify input method",
            choices=[method.value for method in INPUT_METHODS],
            use_shortcuts=True,
            default=INPUT_METHODS.FILE.value,
        ).unsafe_ask()

    if input_method == INPUT_METHODS.SHAPE.value and input_dims is None:
        input_dims = questionary.text(
            "Specify input dimensions for every model input as an array of JSON arrays "
            + '(ie. "[[3, 224, 224]]"), or leave blank to let us try to infer the input sizes")',
            validate=validate_input_dims_json,
            default=str(inferred_input_dims)
            if inferred_input_dims is not None
            else "",
        ).unsafe_ask()

    if input_method == INPUT_METHODS.FILE.value and input_dims is None:
        input_file = questionary.text(
            "Provide an input file path (supported formats: .json)",
            validate=validate_input_file,
            default="",
        ).unsafe_ask()

    normalized_input_dims = normalize_input_dims_for_api(input_dims)

    return (model_name, quantization, normalized_input_dims, input_file)


DEFAULT_MAX_UPLOAD_WORKERS = 4


def common_upload_args(func):
    decorators = [
        click.option(
            "-n",
            "--name",
            "model_name",
            type=str,
            help="Name of the model to be used in AutoDL.",
        ),
        click.option(
            "-t",
            "--quantization",
            "--quants",
            type=click.Choice(supported_quants, case_sensitive=False),
            help="Quantization for the model.",
        ),
        click.option(
            "--input_dims",
            "--input-dims",
            type=str,
            help="The model input dimensions, specified as a JSON array.",
        ),
        click.option(
            "-w",
            "--max_upload_workers",
            type=int,
            help=f"The count of workers to use for multipart uploads; defaults to {DEFAULT_MAX_UPLOAD_WORKERS}.",
            default=DEFAULT_MAX_UPLOAD_WORKERS,
        ),
        click.option(
            "--input-file",
            "--input_file",
            type=str,
            help="The model input filepath.",
        ),
        click.option(
            "-y",
            "--yes",
            "auto_confirm",
            type=bool,
            is_flag=True,
            help="Skip all confirmation input from the user.",
        ),
        click.option(
            "--skip_inputs",
            "--skip-inputs",
            "should_skip_inputs",
            type=bool,
            is_flag=True,
            help="Don't ask about inputs, let AutoDL try to infer them.",
        ),
        options.use_organization_id,
        options.use_quiet_mode,
        click.option(
            "-g",
            "--group_id",
            type=str,
            help="The ID of the model group to add the model to.",
        ),
    ]

    for i in range(len(decorators) - 1, -1, -1):
        func = decorators[i](func)

    return func


@model_commands_group.command()
@options.use_environment
@click.argument(
    "model_file_path",
    type=str,
    # help="File path or HTTP URL to the model file or script",
)
@click.argument(
    "model_script_args",
    type=str,
    nargs=-1,
    # help="Arguments to pass to the model file during load",
)
@common_upload_args
def submit_model(
    organization_id,
    model_file_path: str,
    model_script_args: str,
    model_name: str,
    auto_confirm: bool,
    quiet: bool,
    should_skip_inputs: bool,
    quantization,
    input_dims: Optional[str],
    input_file: Optional[str],
    group_id: str,
    max_upload_workers: int,
    **kwargs,
):
    """Submit a model to AutoDL."""

    # Priority: flags, then configCache, then inference, then interactive user input
    environment = kwargs["environment"]

    (
        model_file,
        inferred_model_name,
        framework,
        inferred_quantization,
        inferred_input_dims,
        is_source_annotated_model,
    ) = analyze_model_file(model_file_path, model_script_args)

    (
        model_name,
        quantization,
        input_dims,
        input_file,
    ) = prompt_for_missing_model_info(
        model_name=model_name,
        quantization=quantization,
        input_dims=input_dims,
        input_file=input_file,
        inferred_model_name=inferred_model_name,
        inferred_quantization=inferred_quantization,
        inferred_input_dims=inferred_input_dims,
        should_skip_inputs=should_skip_inputs,
        is_source_annotated_model=is_source_annotated_model,
    )
    model_config = {
        "name": model_name,
        "framework": framework,
        "quantization": quantization,
        "inputs": input_dims,
        "group_id": group_id,
    }

    if not auto_confirm:
        logger.info("The details for your model are as follows:")
        click.echo(f"{json.dumps(model_config, indent=4)}")
        click.confirm(
            text="\n" + "Do you want to upload it to AutoDL?",
            abort=True,
            default=True,
        )

    model_upload_response = autodl.upload_model(
        environment,
        organization_id,
        model_config,
        model_file,
        input_file_path=input_file,
        max_upload_workers=max_upload_workers,
    )

    announce_model_upload_response(model_upload_response)


supported_model_types = {"GPT-J 6B": "gptj"}


@model_commands_group.command()
@options.use_environment
@click.argument("checkpoint_file_path")
@common_upload_args
@click.option(
    "-t",
    "--model_type",
    type=click.Choice(
        list(supported_model_types.values()), case_sensitive=False
    ),
    default=None,
    help="Type of model",
)
def submit_checkpoint(
    organization_id,
    checkpoint_file_path,
    model_type,
    model_name,
    auto_confirm,
    quantization,
    should_skip_inputs: bool,
    input_dims,
    input_file,
    group_id,
    max_upload_workers,
    **kwargs,
):
    """submit checkpoint to AutoDL"""
    environment = kwargs["environment"]

    if model_type is None:
        model_type_user_choice = questionary.select(
            "Choose one of the supported models for the checkpoint data",
            choices=list(supported_model_types.keys()),
            use_shortcuts=True,
        ).unsafe_ask()
        model_type = supported_model_types[model_type_user_choice]

    framework = "PYTORCH"
    inferred_quantization = None  # nice to have TODO: detect quantization
    inferred_input_dims = None
    inferred_model_name = suggest_model_name(checkpoint_file_path)
    model_filepath = checkpoint_file_path

    (
        model_name,
        quantization,
        input_dims,
        input_file,
    ) = prompt_for_missing_model_info(
        model_name=model_name,
        quantization=quantization,
        input_dims=input_dims,
        input_file=input_file,
        inferred_model_name=inferred_model_name,
        inferred_quantization=inferred_quantization,
        inferred_input_dims=inferred_input_dims,
        should_skip_inputs=should_skip_inputs,
    )
    model_config = {
        "name": model_name,
        "framework": framework,
        "quantization": quantization,
        "inputs": input_dims,
        "group_id": group_id,
    }

    if not auto_confirm:
        logger.info("The details for your model are as follows:")
        click.echo(f"{json.dumps(model_config, indent=4)}")
        click.confirm(
            text="\n" + "Do you want to upload it to AutoDL?",
            abort=True,
            default=True,
        )

    model_filepath = os.path.abspath(model_filepath)

    if os.path.isdir(model_filepath):
        # TODO: add zip progress bar
        time_start = time.time()
        logger.info("Zipping the model checkpoint folder, please wait...")
        zipped_model_file = zipfile.ZipFile(
            os.path.join(".", model_name + ".zip"),
            "w",
            compresslevel=0,
        )
        # write all files in the folder to the zip file
        for root, _, files in os.walk(model_filepath):
            for file in files:
                zipped_model_file.write(
                    os.path.join(root, file),
                    arcname=os.path.join(file),
                )

        model_filepath = zipped_model_file.filename
        logger.info("Zipping finished in %s seconds", time.time() - time_start)
        logger.info("Zipped model file path: %s", model_filepath)
        zipped_model_file.close()

    logger.info("Starting the model upload")
    logger.warning(
        "If the upload isn't utilizing the whole network bandwidth, "
        + "please drop the upload and try again with "
        + "the --max_upload_workers flag set to a higher value "
        + "(currently =%s).",
        max_upload_workers,
    )
    model_upload_response = autodl.upload_model(
        environment,
        organization_id,
        model_config,
        model_filepath,
        input_file_path=input_file,
        model_type=model_type,
        max_upload_workers=max_upload_workers,
    )

    announce_model_upload_response(model_upload_response)

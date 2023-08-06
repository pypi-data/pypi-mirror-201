import sys
import time

import click
import questionary
from questionary import Choice

from autumn8.cli import options, pending_uploads
from autumn8.cli.commands import cloud, models
from autumn8.cli.interactive import (
    announce_model_upload_response,
    fetch_user_data,
)
from autumn8.common._version import __version__
from autumn8.lib.service import resume_upload_model

# from autumn8.cli.cli_environment import CliEnvironment
# from autumn8.common.config.s3 import init_s3_client

# environment = CliEnvironment.STAGING
# s3 = init_s3_client(environment.value.s3_host)
# s3_bucket_name = environment.value.s3_bucket_name
# mpus = s3.list_multipart_uploads(Bucket=s3_bucket_name, MaxUploads=200)

# print("mpus", len(mpus["Uploads"]))
# for mpu in mpus["Uploads"]:
#     print(mpu["Key"])

try:
    current_pending_uploads = pending_uploads.retrieve_pending_uploads()
except (ValueError, AttributeError):
    # data format stored is incompatible with the current version
    # hope that the pending upload will get cleaned up by the S3 lifecycle policy
    # TODO: add the S3 lifecycle policy for that, lol - https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html
    pending_uploads.forget_all_pending_uploads()
    current_pending_uploads = {}

# TODO: save costs by configuring https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html
# TODO: detect if the cached upload is still available on S3; forget it if it got cleaned up
for key in current_pending_uploads:
    resume_args = current_pending_uploads[key]
    print("You have pending upload of {}".format(resume_args["model_file"]))
    continue_upload = questionary.select(
        "Do you want to continue upload?",
        choices=[
            Choice(title="Yes", value="Y"),
            Choice(title="No", value="n"),
            Choice(title="Drop upload", value="drop"),
        ],
        use_shortcuts=True,
    ).unsafe_ask()

    if continue_upload == "" or continue_upload == "Y":
        model_upload_response = resume_upload_model(
            {**resume_args, **resume_args["kwargs"]}
        )
        announce_model_upload_response(model_upload_response)
        sys.exit(0)

    if continue_upload == "drop":
        pending_uploads.abort_and_forget_upload(resume_args["run_id"])


@options.use_environment
def test_connection(environment):
    """
    Test AutoDL connection with the current API key.
    Displays the user's email address upon successful connection.
    """
    user_data = fetch_user_data(environment)
    print(f"Hello! You're authenticated as {user_data['email']}")


@click.group()
@click.version_option(version=__version__)
def main():
    pass


main.command()(test_connection)

all_commands = []

for command in [
    *models.model_commands_group.commands.values(),
    *cloud.cloud_commands_group.commands.values(),
]:
    main.add_command(command)


if __name__ == "__main__":
    main()

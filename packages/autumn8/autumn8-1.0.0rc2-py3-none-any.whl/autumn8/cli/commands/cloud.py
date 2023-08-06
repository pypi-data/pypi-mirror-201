import json

import click

from autumn8.cli import options
from autumn8.cli.cli_environment import CliEnvironment
from autumn8.common.config.settings import CloudServiceProvider
from autumn8.common.config.supported_instances import find_instance_config
from autumn8.common.types import DEFAULT_CLOUD_ZONES_CONFIG
from autumn8.lib import logging
from autumn8.lib.api import cloud

logger = logging.getLogger(__name__)


@click.group()
def cloud_commands_group():
    pass


@cloud_commands_group.command()
@options.use_environment
@options.use_organization_id
@options.use_quiet_mode
@options.use_cloud_provider_picker(optional=True)
@click.option(
    "-m",
    "--model_id",
    help="Model ID to get the deployments for",
    prompt_required=False,
    default=None,
)
def list_deployments(
    organization_id,
    model_id,
    environment: CliEnvironment,
    cloud_provider,
    quiet,
):
    """List running deployments."""
    logger.info("Fetching the list of deployments...")
    deployments = cloud.get_running_deployments(
        organization_id,
        environment,
        model_id=model_id,
        service_provider=cloud_provider,
    )

    click.echo(json.dumps(deployments, indent=4))
    return


@cloud_commands_group.command()
@click.option(
    "-hw",
    "-t",
    "--machine_type",
    prompt="Machine type (ie. c5.2xlarge)",
    type=str,
    help="Server type to use for the deployment",
    # TODO: add a better interactive prompt listing all available servers
)
@options.use_environment
@options.use_organization_id
@options.use_quiet_mode
@click.option(
    "-m",
    "--model_id",
    "--model-id",
    prompt=True,
    type=int,
    help="Model ID to deploy",
    # TODO: add a better interactive prompt listing all available models
)
@options.use_cloud_provider_picker(optional=False)
def deploy(
    organization_id: int,
    model_id: int,
    machine_type: str,
    environment: CliEnvironment,
    cloud_provider: CloudServiceProvider,
    quiet,
):
    """Deploy a model from AutoDL onto cloud."""
    instance_config = find_instance_config(
        machine_type, fetch_data_from_cloud_info=False
    )
    real_hardware_provider = instance_config.service_provider
    logger.info(
        "Launching a new deployment onto %s...",
        DEFAULT_CLOUD_ZONES_CONFIG[real_hardware_provider],
    )
    deployments = cloud.deploy(
        organization_id,
        environment,
        machine_type=machine_type,
        service_provider=cloud_provider,
        model_id=model_id,
    )

    click.echo(json.dumps(deployments, indent=4))


@cloud_commands_group.command()
@options.use_environment
@options.use_organization_id
@options.use_quiet_mode
@options.use_cloud_provider_picker(optional=False)
@click.option(
    "-d",
    "--deployment_id",
    prompt=True,
    help="ID of the deployment to terminate",
)
def terminate_deployment(
    organization_id,
    deployment_id,
    environment: CliEnvironment,
    cloud_provider,
    quiet,
):
    """Terminate a running deployment."""
    response = cloud.terminate_deployment(
        organization_id, environment, deployment_id, cloud_provider
    )
    click.echo(json.dumps(response, indent=4))

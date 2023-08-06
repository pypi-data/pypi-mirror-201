from typing import Dict

from autumn8.common.config.settings import CloudServiceProvider

ZoneConfig = Dict[CloudServiceProvider, str]

DEFAULT_CLOUD_ZONES_CONFIG: ZoneConfig = {
    CloudServiceProvider.AMAZON: "us-east-1",
    CloudServiceProvider.GOOGLE: "us-central1",
    CloudServiceProvider.ORACLE: "us-sanjose-1",
    CloudServiceProvider.AZURE: "useast",
}

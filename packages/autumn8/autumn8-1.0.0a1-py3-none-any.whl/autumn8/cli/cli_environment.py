import enum
from dataclasses import dataclass
from typing import Optional


@dataclass
class EnvironmentProperties:
    app_host: str
    s3_host: str
    s3_bucket_name: str
    s3_bucket_root_folder: Optional[str]


# TODO remove - official CLI builds should only point toward production


class CliEnvironment(enum.Enum):
    value: EnvironmentProperties
    LOCALHOST = EnvironmentProperties(
        app_host="http://localhost",
        s3_host="http://localhost:4566",
        s3_bucket_name="predictor-bucket",
        s3_bucket_root_folder=None,
    )
    STAGING = EnvironmentProperties(
        app_host="http://staging.autumn8.ai",
        s3_host="https://s3-accelerate.amazonaws.com",
        s3_bucket_name="autodl-staging",
        s3_bucket_root_folder="autodl-staging",
    )
    PRODUCTION = EnvironmentProperties(
        app_host="https://autodl.autumn8.ai",
        s3_host="https://s3-accelerate.amazonaws.com",
        s3_bucket_name="autodl-staging",
        s3_bucket_root_folder="autodl-production",
    )

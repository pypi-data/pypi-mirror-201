from pathlib import Path
from enum import Enum
import logging
from pydantic import BaseSettings
from . import logs

parent_dir = Path(__file__).absolute().parent
base_dir = parent_dir.parent

logger = logs.create_logger(name="config", level=logging.DEBUG)


class Env(str, Enum):
    SANDBOX = "sandbox"
    LIVE = "live"


class Platform(str, Enum):
    LOCAL = "local"

    CLOUD_RUN = "cloudrun"
    RAILWAY = "railway"

    APP_RUNNER = "app_runner"
    LAMBDA = "lambda"
    HEROKU = "heroku"

    PORTER_AWS = "porter_aws"
    PORTER_GCP = "porter_gcp"
    PORTER_DO = "porter_do"

    ZEET_CLOUDRUN = "zeet_cloudrun"


class AppSettings(BaseSettings):
    api_prefix: str = "/api/v1"
    app_name_prefix: str = "quilt"
    version: str = "0.1.0"


class SentrySettings(BaseSettings):
    sentry_dsn: str


class Settings(AppSettings, SentrySettings):
    env: Env
    branch: str

    platform: Platform
    base_dir: Path = base_dir

    @property
    def app_name(self) -> str:
        return f"{self.app_name_prefix} {self.branch}-{self.env.value} on {self.platform.value}"

    def is_live(self) -> bool:
        return self.env == Env.LIVE

    def is_sandbox(self) -> bool:
        return self.env == Env.SANDBOX

from fluvii.apps import FluviiAppConfig
from fluvii.config_bases import FluviiConfigBase
from nubium_utils.fluvii_extensions.components.sqlite import NubiumSqliteConfig
from nubium_utils.fluvii_extensions.components.auth import NubiumAuthKafkaConfig
from typing import Optional
from pydantic import BaseSettings


class NubiumRetryConfig(BaseSettings):
    input_topic: Optional[str] = None
    success_output_topic: Optional[str] = None
    retry_output_topic: Optional[str] = None
    failure_output_topic: Optional[str] = None
    retry_count_max: Optional[int] = 0

    class Config(FluviiConfigBase.Config):
        env_prefix = "NUBIUM_RETRY_APP_"


class AppCfgUpdatedDefaults(FluviiAppConfig):
    sqlite_config: NubiumSqliteConfig = NubiumSqliteConfig()
    auth_config: NubiumAuthKafkaConfig = NubiumAuthKafkaConfig()


class NubiumAppConfig(AppCfgUpdatedDefaults):
    retry_configs: NubiumRetryConfig = NubiumRetryConfig()

    class Config(AppCfgUpdatedDefaults.Config):
        @classmethod
        def prepare_field(cls, field) -> None:
            """
            This allows you to preserve the env_prefix for the inhereted config values
            while using only the new env_prefix for exclusively the new config values.
            They are mutually exclusive so you must use the specified prefix for that given set of config values.
            You can override existing config values with new defaults, but they will then require the new env_prefix.
            Passing in config values via arguments still works as expected.
            """
            if 'env_names' in field.field_info.extra:
                return
            return super().prepare_field(field)

        env_prefix = "NUBIUM_APP_"

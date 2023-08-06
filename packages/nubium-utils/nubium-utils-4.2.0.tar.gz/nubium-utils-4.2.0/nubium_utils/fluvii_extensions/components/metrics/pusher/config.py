from fluvii.components.metrics.pusher import MetricsPusherConfig
from pydantic import validator
from typing import Union


class UpdatedPusherDefaults(MetricsPusherConfig):
    kubernetes_headless_service_port: Union[str, int] = 8080
    kubernetes_pod_app_port: Union[str, int] = 9091


class NubiumMetricsPusherConfig(UpdatedPusherDefaults):
    kubernetes_namespace: str

    @validator('kubernetes_headless_service_name')
    def set_headless_service_name(cls, value, values):
        if not value:
            return f'bifrost-metrics-cache-headless.{values["kubernetes_namespace"]}.svc.cluster.local'
        return value

    class Config(UpdatedPusherDefaults.Config):
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

        env_prefix = "NUBIUM_METRICS_PUSHER_"

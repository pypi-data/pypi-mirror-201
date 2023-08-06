from fluvii.components.consumer import ConsumerConfig
from nubium_utils.fluvii_extensions.components.auth import NubiumAuthKafkaConfig


class NubiumConsumerConfig(ConsumerConfig):
    timestamp_offset_minutes: int = 0
    auth_config = NubiumAuthKafkaConfig = NubiumAuthKafkaConfig()

    class Config(ConsumerConfig.Config):
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

        env_prefix = 'NUBIUM_CONSUMER_'

    def as_client_dict(self):
        client_dict = super().as_client_dict()
        ms_tolerance = 1_000
        heartbeat_timeout_with_offset = (60*self.timestamp_offset_minutes) + self.heartbeat_timeout_seconds
        timeout_minutes_with_offset = self.timestamp_offset_minutes + self.timeout_minutes
        client_dict.update({
            "heartbeat.interval.ms": ((heartbeat_timeout_with_offset // 5) * 1_000) - ms_tolerance,
            "max.poll.interval.ms": timeout_minutes_with_offset * 60_000,
            "session.timeout.ms": heartbeat_timeout_with_offset * 1_000,
        })
        return client_dict

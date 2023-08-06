from fluvii.components.producer import ProducerConfig
from nubium_utils.fluvii_extensions.components.auth import NubiumAuthKafkaConfig


class NubiumProducerConfig(ProducerConfig):
    auth_config: NubiumAuthKafkaConfig = NubiumAuthKafkaConfig()

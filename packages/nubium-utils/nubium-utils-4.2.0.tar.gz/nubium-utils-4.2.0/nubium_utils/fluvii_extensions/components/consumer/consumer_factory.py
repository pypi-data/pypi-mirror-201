from . import NubiumConsumer, NubiumConsumerConfig
from fluvii.components.consumer import ConsumerFactory
from nubium_utils.fluvii_extensions.components.metrics import NubiumMetricsManager, NubiumMetricsManagerConfig


class NubiumConsumerFactory(ConsumerFactory):
    consumer_cls = NubiumConsumer
    consumer_config_cls = NubiumConsumerConfig
    metrics_cls = NubiumMetricsManager
    metrics_config_cls = NubiumMetricsManagerConfig


from fluvii.components.producer import ProducerFactory
from nubium_utils.fluvii_extensions.components.metrics import NubiumMetricsManager, NubiumMetricsManagerConfig
from .config import NubiumProducerConfig


class NubiumProducerFactory(ProducerFactory):
    metrics_cls = NubiumMetricsManager
    metrics_config_cls = NubiumMetricsManagerConfig
    producer_config_cls = NubiumProducerConfig

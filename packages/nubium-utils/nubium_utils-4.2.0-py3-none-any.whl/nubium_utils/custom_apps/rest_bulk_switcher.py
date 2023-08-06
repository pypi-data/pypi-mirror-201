from nubium_utils.fluvii_extensions.apps.nubium_multi_msg_app import NubiumMultiMessageAppFactory
from nubium_utils.fluvii_extensions.components.consumer import NubiumConsumerConfig
import logging

LOGGER = logging.getLogger(__name__)


class NubiumRestBulkSwitcherConsumerConfig(NubiumConsumerConfig):
    """Didn't want to hardcode, but did need to change values to have this function reasonably"""
    batch_consume_trigger_message_age_seconds: int = 60
    batch_consume_max_time_seconds: int = 120


class NubiumRestBulkSwitcherFactory(NubiumMultiMessageAppFactory):
    consumer_config_cls = NubiumRestBulkSwitcherConsumerConfig

    def _make_consumer(self):
        LOGGER.warning(f'By default, there are some hard-coded consumer settings for {self.__class__.__name__} '
                       'that will override any corresponding configuration settings to ensure expected functionality')
        self._consumer_config.batch_consume_max_count = 0
        return super()._make_consumer()

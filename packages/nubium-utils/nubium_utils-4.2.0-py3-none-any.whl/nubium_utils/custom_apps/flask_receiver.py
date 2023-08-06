from os import environ
from unittest import mock
from nubium_utils.fluvii_extensions.components.producer import NubiumProducerFactory
from nubium_utils.fluvii_extensions.components.metrics import NubiumMetricsManagerConfig
import threading
import time


class NubiumFlaskConfig:
    def __init__(self, producer=None, topic=None, schema=None, producer_config=None, metrics_config=None):
        self.LOGLEVEL = environ.get('NUBIUM_LOGLEVEL', 'INFO')

        self.TOPIC = topic
        self.PRODUCER = producer
        self.SCHEMA = schema

        if self.TOPIC is None:
            self.TOPIC = environ['OUTPUT_TOPIC']

        self.TOPIC_SCHEMA_DICT = {self.TOPIC: self.SCHEMA}

        if self.PRODUCER is None:
            if not metrics_config:
                metrics_config = NubiumMetricsManagerConfig()  # enforces variables are set so the metrics manager works
            self.PRODUCER = NubiumProducerFactory(
                topic_schema_dict=self.TOPIC_SCHEMA_DICT,
                producer_config=producer_config,
                metrics_manager_config=metrics_config)
        self.METRICS_MANAGER = self.PRODUCER.metrics_manager

        self.PRODUCER_POLL_THREAD = threading.Thread(target=self._producer_poll_loop, daemon=True)
        self.PRODUCER_POLL_THREAD.start()

    def _producer_poll_loop(self):
        """So we dont get spammed with (harmless) re-auth errors"""
        while True:
            try:
                self.PRODUCER.poll(0)
            except:
                pass
            time.sleep(10)


class NubiumTestFlaskConfig:
    def __init__(self):
        self.TESTING = True
        self.LOGLEVEL = "DEBUG"
        self.TOPIC = mock.MagicMock()
        self.SCHEMA = mock.MagicMock()
        self.METRICS_MANAGER = mock.MagicMock()
        self.PRODUCER = mock.MagicMock()

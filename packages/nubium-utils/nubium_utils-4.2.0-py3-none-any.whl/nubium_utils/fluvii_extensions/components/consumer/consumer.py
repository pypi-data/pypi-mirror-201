from fluvii.components.consumer import Consumer
from time import sleep
import datetime
import logging


LOGGER = logging.getLogger(__name__)


class NubiumConsumer(Consumer):
    def _wait_until_message_offset_time(self):
        """
        Wait until the message's timestamp + the deployments offset before handling
        """
        if wait_minutes := self._config.timestamp_offset_minutes:
            message_process_time = (self.message.timestamp()[1] // 1000) + (wait_minutes * 60)
            wait_time = int(message_process_time - datetime.datetime.timestamp(datetime.datetime.utcnow()))
            if wait_time:
                LOGGER.info(f'Waiting {wait_time} seconds before message processing continues; GUID {self.headers()["guid"]}')
                sleep(wait_time)
                return 'i sleep'
        return 'real shit'

    def _handle_consumed_message(self):
        super()._handle_consumed_message()
        self._wait_until_message_offset_time()

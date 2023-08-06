from fluvii.apps.transactions.transaction import Transaction, TableTransaction
import logging
import json

LOGGER = logging.getLogger(__name__)


class NubiumTransaction(Transaction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._retry = self.app._config.retry_configs

    def produce_retry(self, exception=None):
        headers = self.headers()
        guid = headers['guid']
        kafka_retry_count = int(headers.get('kafka_retry_count', '0'))

        if kafka_retry_count < self._retry.retry_count_max:
            headers['kafka_retry_count'] = str(kafka_retry_count + 1)
            retry_topic = self._retry.input_topic
        else:
            headers['kafka_retry_count'] = '0'
            retry_topic = self._retry.retry_output_topic

        if retry_topic:
            if not exception:
                exception = self.RetryTopicSend()
            LOGGER.warning('; '.join([str(exception), f'retrying GUID {guid}']))
            self.produce(dict(value=self.value(), topic=retry_topic, headers=headers))

        else:
            if not exception:
                exception = self.FailureTopicSend()
            LOGGER.error('; '.join([str(exception), f'GUID {guid}']))
            self.produce_failure(exception=self.MaxRetriesReached())

    def produce_failure(self, exception=None):
        headers = self.headers()
        guid = headers['guid']
        headers['kafka_retry_count'] = '0'

        if not exception:
            exception = self.FailureTopicSend()
        LOGGER.error('; '.join([type(exception).__name__, str(exception), f'failing GUID {guid}']))
        headers["exception"] = json.dumps({"name": type(exception).__name__, "description": str(exception)})

        LOGGER.debug(f'Adding a message to the produce queue for deadletter/failure topic {self._retry.failure_output_topic}')
        self.produce(dict(value=self.value(), topic=self._retry.failure_output_topic, headers=headers))
        LOGGER.info(f'Message added to the deadletter/failure topic produce queue; GUID {guid}')

    class MaxRetriesReached(Exception):
        """
        Represents that all retry attempts for a retry-looped app have failed.
        """

        def __init__(self, *args):
            if not args:
                default_message = "All app retry attempts have failed"
                args = (default_message,)
            super().__init__(*args)

    class RetryTopicSend(Exception):
        """
        Represents that an external call has failed but further retries will be attempted.
        Only a placeholder for logging a message sent to a retry topic when the app did not provide an explicit exception.
        """

        def __init__(self, *args):
            if not args:
                default_message = "External call attempt has failed, but will retry."
                args = (default_message,)
            super().__init__(*args)

    class FailureTopicSend(Exception):
        """
        Represents that an external call has failed and no further retries will be attempted.
        Only a placeholder for logging a message sent to a failure topic when the app did not provide an explicit exception.
        """

        def __init__(self, *args):
            if not args:
                default_message = "External call attempt has failed and no (additional?) retries will be attempted."
                args = (default_message,)
            super().__init__(*args)


class NubiumTableTransaction(TableTransaction, NubiumTransaction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # like magic, this adds self._retry too...thanks super MRO!

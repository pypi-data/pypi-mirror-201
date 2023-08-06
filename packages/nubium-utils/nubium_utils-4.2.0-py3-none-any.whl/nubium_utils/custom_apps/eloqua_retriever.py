from nubium_utils.fluvii_extensions.apps.nubium_table_app import NubiumTableAppFactory, NubiumTableApp
from nubium_utils.fluvii_extensions.apps.transactions import NubiumTableTransaction
from nubium_utils.fluvii_extensions.components.consumer import NubiumConsumerConfig
from fluvii.exceptions import FinishedTransactionBatch, PartitionsAssigned, TransactionNotRequired
import logging


LOGGER = logging.getLogger(__name__)


class NubiumEloquaRetrieverConsumerConfig(NubiumConsumerConfig):
    """Didn't want to hardcode a new timeout"""
    timeout_minutes: int = 5


class EloquaRetrieverTransaction(NubiumTableTransaction):
    """
    Necessary because we aren't usually consuming a message while producing table messages. We can mock out what
    we would need from a message by returning static values for the necessary items called.
    """
    def key(self):
        return 'timestamp'

    def headers(self):
        try:
            return super().headers()
        except Exception:
            return {'guid': 'none', 'last_updated_by': 'self'}

    def partition(self):
        return 0


class NubiumEloquaRetrieverApp(NubiumTableApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, transaction_cls=EloquaRetrieverTransaction)

    def _handle_message(self, **kwargs):
        self.consume(**kwargs)
        timestamp = self.transaction.value()['timestamp']
        LOGGER.info(f'External lowerbound timestamp received: {timestamp} UTC')
        table_entry = self.transaction.read_table_entry()
        table_entry.update({'lowerbound': timestamp, 'ebb': ''})
        self.transaction.update_table_entry(table_entry)

    def _no_message_callback(self):
        self._producer.poll(0)
        self._app_function(self.transaction, *self._app_function_arglist)
        try:
            self._finalize_app_batch()
            self.commit_tables()
        except TransactionNotRequired:  # Means it's waiting on an update from EBB or Eloqua's tracker record
            pass

    def _run(self, **kwargs):
        self._init_transaction_handler()
        assignments = self._consumer.assignment()
        while len(assignments) != 2:
            try:
                self.consume(**kwargs)
            except FinishedTransactionBatch:
                self._producer.poll(0)
                LOGGER.info('Waiting on rebalance to complete...')
            except PartitionsAssigned:
                self._handle_rebalance()
            finally:
                assignments = self._consumer.assignment()
        super()._run(**kwargs)


class NubiumEloquaRetrieverAppFactory(NubiumTableAppFactory):
    fluvii_app_cls = NubiumEloquaRetrieverApp
    consumer_config_cls = NubiumEloquaRetrieverConsumerConfig

    def _make_consumer(self, auto_subscribe=False):
        LOGGER.warning(f'By default, there are some hard-coded consumer settings for {self.__class__.__name__} '
                       'that will override any corresponding configuration settings to ensure expected functionality')
        self._consumer_config.poll_timeout_seconds = 5
        self._consumer_config.batch_consume_max_time_seconds = 4
        return super()._make_consumer(auto_subscribe=auto_subscribe)

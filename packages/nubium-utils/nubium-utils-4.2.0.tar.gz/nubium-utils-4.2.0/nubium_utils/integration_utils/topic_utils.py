import logging
from importlib import import_module
from os import environ
from time import sleep
import pytest
from fluvii.kafka_tools import FluviiToolbox

LOGGER = logging.getLogger(__name__)


kafka_toolbox = FluviiToolbox()


@pytest.fixture()
def create_topics(topics):
    LOGGER.info(f"Creating topics...\n{topics}")
    kafka_toolbox.create_topics(topics.replace(" ", "").split(","))


@pytest.fixture()
def delete_topics(topics):
    LOGGER.info(f"Deleting topics to start fresh...\n{topics}")
    kafka_toolbox.delete_topics(topics.replace(" ", "").split(","))


@pytest.fixture()
def delete_test_topics():
    kafka_toolbox.delete_topics([v for k, v in environ.items() if '_TOPIC' in k and v.startswith('TEST__')])
    sleep(3)


@pytest.fixture()
def create_test_topics():
    topic_dict = {
        topic: {'partitions': 1, 'replication.factor': 3}
        for topic in [v for k, v in environ.items() if '_TOPIC' in k and v.startswith('TEST__')]}
    kafka_toolbox.create_topics(topic_dict)
    sleep(2)


@pytest.fixture()
def produce_input(map_kafka_input):
    LOGGER.info("Producing test messages to the input topic...")
    import_path, obj = environ['INPUT_SCHEMA'].rsplit('.', 1)
    kafka_toolbox.produce_messages(
        {environ['INPUT_TOPIC']: getattr(import_module(import_path), obj)},
        map_kafka_input,
        topic_override=environ['INPUT_TOPIC'])
    sleep(10)  # wait for app to process the messages


def format_message(bulk_transaction):
    return [{'key': msg.key(), 'value': msg.value(), 'headers': {key: value.decode("utf-8") for key, value in dict(msg.headers()).items()}} for msg in bulk_transaction.messages()]


@pytest.fixture()
def consume_output():
    LOGGER.info("Consuming test messages from the output topic...")
    return kafka_toolbox.consume_messages({environ['OUTPUT_TOPIC']: {}}, transform_function=format_message)

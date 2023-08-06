import logging
from os import environ, path
from shutil import rmtree
from time import sleep
from nubium_utils.test_utils.run_app import run_app

import psutil
import pytest


LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def app_wait():
    sleep(10)


@pytest.fixture()
def process_wait():
    sleep(10)


@pytest.fixture()
def delete_app_table():
    if path.exists(environ['FLUVII_SQLITE_TABLE_DIRECTORY']):
        rmtree(environ['FLUVII_SQLITE_TABLE_DIRECTORY'])


@pytest.fixture()
def setup_app(request):
    # optional args, set via @pytest.mark.parametrize('setup_app', [{'env_overrides': {'var': 'val'}}], indirect=True)
    kwargs = {'env_overrides': None}
    kwargs.update(getattr(request, 'param', {}))

    LOGGER.info("Initializing app...")
    parent = run_app(runtime_env_overrides=kwargs['env_overrides'])  # skip sync since it happens before running integration
    sleep(15)  # wait for app to launch
    return parent


@pytest.fixture()
def teardown_app(setup_app):
    LOGGER.info("Terminating app...")
    children = psutil.Process(setup_app)
    for child in children.children(recursive=True):
        child.terminate()
    sleep(10)  # wait for app to fully stop

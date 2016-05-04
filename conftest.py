import logging

import pytest

import vanth.config
import vanth.tables
from vanth.server import create_app

LOGGER = logging.getLogger(__name__)

def pytest_cmdline_main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

@pytest.fixture(scope='session')
def tables():
    return vanth.tables

@pytest.fixture
def app(configuration):
    _app = create_app(configuration)
    _app.config['TESTING'] = True
    return _app

@pytest.fixture(scope="session")
def db_connection_uri(configuration):
    return configuration.db

@pytest.fixture(scope='session')
def config_specification():
    return vanth.config.SPECIFICATION

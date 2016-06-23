import logging
import os

import chryso.connection
import sepiida.config
import sepiida.log

import vanth.config
import vanth.server
import vanth.tables

LOGGER = logging.getLogger(__name__)

def create_db_connection(config):
    engine = chryso.connection.Engine(config.db, vanth.tables)
    chryso.connection.store(engine)
    return engine

def create_application(config):
    create_db_connection(config)
    LOGGER.info("Starting up vanth version %s", vanth.version.VERSION)
    application = vanth.server.create_app(config)

    logging.getLogger('vanth.cors').setLevel(logging.WARNING)

    return application

def setup_logging():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig()

    sepiida.log.setup_logging()
    logging.getLogger('vanth.sgml').setLevel(logging.INFO)

def get_config():
    return sepiida.config.load('/etc/vanth.yaml', vanth.config.SPECIFICATION)

def main():
    setup_logging()
    config = get_config()

    application = create_application(config)
    try:
        host = os.getenv('HOST', 'localhost')
        port = int(os.getenv('PORT', 4545))
        application.run(host, port)
    except KeyboardInterrupt:
        LOGGER.info('Shutting down')

import logging
import os

import chryso.connection
import sepiida.config
import sepiida.log

import vanth.config
import vanth.server
import vanth.tables

LOGGER = logging.getLogger(__name__)

def create_application(config):
    sepiida.log.setup_logging()
    engine = chryso.connection.Engine(config.db, vanth.tables)
    chryso.connection.store(engine)

    LOGGER.info("Starting up vanth version %s", vanth.version.VERSION)
    application = vanth.server.create_app(config)

    logging.getLogger('vanth.cors').setLevel(logging.WARNING)

    return application

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig()

    config = sepiida.config.load('/etc/vanth.yaml', vanth.config.SPECIFICATION)
    application = create_application(config)
    try:
        host = os.getenv('HOST', 'localhost')
        port = int(os.getenv('PORT', 4545))
        application.run(host, port)
    except KeyboardInterrupt:
        LOGGER.info('Shutting down')

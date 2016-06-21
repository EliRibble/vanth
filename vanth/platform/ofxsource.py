import logging

import chryso.connection

import vanth.tables

LOGGER = logging.getLogger(__name__)

def get():
    engine = chryso.connection.get()
    query = vanth.tables.OFXSource.select()
    results = engine.execute(query).fetchall()
    return [dict(result) for result in results]

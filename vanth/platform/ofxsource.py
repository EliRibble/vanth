import logging

import chryso.connection

import vanth.tables

LOGGER = logging.getLogger(__name__)

def _query_and_convert(query):
    engine = chryso.connection.get()
    results = engine.execute(query).fetchall()
    return [dict(result) for result in results]

def by_uuid(uuid):
    query = vanth.tables.OFXSource.select().where(vanth.tables.OFXSource.c.uuid == uuid)
    return _query_and_convert(query)

def get():
    query = vanth.tables.OFXSource.select()
    return _query_and_convert(query)

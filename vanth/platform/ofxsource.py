import logging
import uuid

import chryso.connection
import sqlalchemy

import vanth.tables

LOGGER = logging.getLogger(__name__)

def _query_and_convert(query):
    engine = chryso.connection.get()
    results = engine.execute(query).fetchall()
    return [dict(result) for result in results]

def by_uuid(uuid_):
    query = vanth.tables.OFXSource.select().where(vanth.tables.OFXSource.c.uuid == uuid_)
    return _query_and_convert(query)

def get():
    query = vanth.tables.OFXSource.select()
    return _query_and_convert(query)

def ensure_exist(institutions):
    engine = chryso.connection.get()
    query = sqlalchemy.select([
        vanth.tables.OFXSource.c.fid,
    ])
    results = engine.execute(query).fetchall()
    LOGGER.debug("Found %d OFX sources", len(results))
    known_records = {result[vanth.tables.OFXSource.c.fid] for result in results}
    new_records = [institution for institution in institutions if institution['fid'] not in known_records]
    LOGGER.debug("Have %d new transactions to save", len(new_records))
    to_insert = [{
        'name'        : institution['name'],
        'fid'         : institution['fid'],
        'url'         : institution['url'],
        'uuid'        : str(uuid.uuid4()),
    } for institution in new_records]
    if to_insert:
        engine.execute(vanth.tables.OFXSource.insert(), to_insert) # pylint: disable=no-value-for-parameter
        LOGGER.debug("Done inserting %d records", len(new_records))
    else:
        LOGGER.debug("Not performing insert, nothing to do")

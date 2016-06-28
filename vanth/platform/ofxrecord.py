import logging
import uuid

import chryso.connection
import sqlalchemy

import vanth.tables

LOGGER = logging.getLogger(__name__)

def ensure_exists(account, transactions):
    engine = chryso.connection.get()
    query = sqlalchemy.select([
        vanth.tables.OFXRecord.c.fid,
    ]).where(vanth.tables.OFXRecord.c.ofxaccount == account['uuid'])
    results = engine.execute(query).fetchall()
    LOGGER.debug("Found %d OFX records for %s", len(results), account)
    known_records = {result[vanth.tables.OFXRecord.c.fid] for result in results}
    new_records = [transaction for transaction in transactions if transaction.id not in known_records]
    LOGGER.debug("Have %d new transactions to save", len(new_records))
    to_insert = [{
        'amount'        : transaction.amount,
        'available'     : transaction.available,
        'fid'           : transaction.id,
        'memo'          : transaction.memo,
        'name'          : transaction.name,
        'ofxaccount'    : account['uuid'],
        'posted'        : transaction.posted,
        'type'          : transaction.type,
        'uuid'          : uuid.uuid4(),
    } for transaction in new_records]
    if to_insert:
        engine.execute(vanth.tables.OFXRecord.insert(), to_insert) # pylint: disable=no-value-for-parameter
        LOGGER.debug("Done inserting %d records", len(new_records))

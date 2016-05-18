import logging

import chryso.connection
import sepiida.routing

import vanth.tables

LOGGER = logging.getLogger(__name__)

def by_filter(filters):
    engine = chryso.connection.get()
    LOGGER.debug("Getting ofxsources by filter %s", filters)
    query = vanth.tables.OFXSource.select()
    results = engine.execute(query).fetchall()
    return [{
        'name'      : result[vanth.tables.OFXSource.c.name],
        'fid'       : result[vanth.tables.OFXSource.c.fid],
        'bankid'    : result[vanth.tables.OFXSource.c.bankid],
        'uri'       : sepiida.routing.uri('ofxsource', result[vanth.tables.OFXSource.c.uuid]),
    } for result in results]

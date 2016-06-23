import uuid

import chryso.connection
import sqlalchemy

import vanth.platform.ofxsource
import vanth.tables


def get(user_id):
    engine = chryso.connection.get()
    query = sqlalchemy.select([
        vanth.tables.OFXSource.c.name.label('institution'),
        vanth.tables.OFXAccount.c.name,
        vanth.tables.OFXAccount.c.source,
        vanth.tables.OFXAccount.c.type,
        vanth.tables.OFXAccount.c.user_id,
        vanth.tables.OFXAccount.c.uuid,
    ]).where(
        vanth.tables.OFXAccount.c.source == vanth.tables.OFXSource.c.uuid
    )
    if user_id:
        query = query.where(
            vanth.tables.OFXAccount.c.owner == user_id
        )
    results = engine.execute(query)
    return [{
        'institution'   : result[vanth.tables.OFXSource.c.name.label('institution')],
        'name'          : result[vanth.tables.OFXAccount.c.name],
        'source'        : result[vanth.tables.OFXAccount.c.source],
        'type'          : result[vanth.tables.OFXAccount.c.type],
        'user_id'       : result[vanth.tables.OFXAccount.c.user_id],
        'uuid'          : result[vanth.tables.OFXAccount.c.uuid],
    } for result in results]

def create(values):
    engine = chryso.connection.get()

    values['source'] = sqlalchemy.select([
        vanth.tables.OFXSource.c.uuid
    ]).where(vanth.tables.OFXSource.c.name == values.pop('institution'))

    values['uuid'] = uuid.uuid4()
    statement = vanth.tables.OFXAccount.insert().values(**values) # pylint: disable=no-value-for-parameter
    engine.execute(statement)
    return values['uuid']

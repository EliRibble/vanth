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
    ).where(
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

def create(user_id, name, account_type, institution, password, account_user):
    engine = chryso.connection.get()

    source_name = sqlalchemy.select([
        vanth.tables.OFXSource.c.uuid
    ]).where(vanth.tables.OFXSource.c.name == institution)

    _uuid = uuid.uuid4()
    statement = vanth.tables.OFXAccount.insert().values( # pylint: disable=no-value-for-parameter
        uuid        = _uuid,
        name        = name,
        user_id     = account_user,
        password    = password,
        type        = account_type,
        source      = source_name,
        owner       = user_id,
    )
    engine.execute(statement)
    return _uuid

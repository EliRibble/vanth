import logging
import uuid

import chryso.connection
import sqlalchemy
import sqlalchemy.sql.functions

import vanth.platform.ofxsource
import vanth.tables

LOGGER = logging.getLogger(__name__)

def _select():
    my_max = sqlalchemy.sql.functions.max(vanth.tables.OFXUpdate.c.created)
    subselect = sqlalchemy.select([
        vanth.tables.OFXUpdate.c.ofxaccount,
        my_max,
    ]).limit(1).group_by(
        vanth.tables.OFXUpdate.c.ofxaccount
    ).alias('ofxupdates')
    return sqlalchemy.select([
        vanth.tables.OFXAccount.c.account_id,
        vanth.tables.OFXAccount.c.name,
        vanth.tables.OFXAccount.c.password,
        vanth.tables.OFXAccount.c.source,
        vanth.tables.OFXAccount.c.type,
        vanth.tables.OFXAccount.c.user_id,
        vanth.tables.OFXAccount.c.uuid,
        vanth.tables.OFXSource.c.name.label('source.name'),
        vanth.tables.OFXSource.c.uuid.label('source.uuid'),
        subselect,
    ]).select_from(
        subselect
    ).where(
        vanth.tables.OFXAccount.c.uuid == subselect.c.ofxaccount
    )

def _execute_and_convert(query):
    engine = chryso.connection.get()
    results = engine.execute(query)
    return [{
        'account_id'    : result[vanth.tables.OFXAccount.c.account_id],
        'name'          : result[vanth.tables.OFXAccount.c.name],
        'last_updated'  : result['max_1'],
        'password'      : result[vanth.tables.OFXAccount.c.password],
        'source'        : {
            'name'      : result[vanth.tables.OFXSource.c.name.label('source.name')],
            'uuid'      : result[vanth.tables.OFXSource.c.name.label('source.uuid')],
        },
        'type'          : result[vanth.tables.OFXAccount.c.type],
        'user_id'       : result[vanth.tables.OFXAccount.c.user_id],
        'uuid'          : result[vanth.tables.OFXAccount.c.uuid],
    } for result in results]

def by_uuid(account_uuid):
    query = _select().where(vanth.tables.OFXAccount.c.uuid == account_uuid)
    account = _execute_and_convert(query)
    return account[0] if account else None

def by_user(user_id):
    query = _select()
    if user_id:
        query = query.where(
            vanth.tables.OFXAccount.c.owner == user_id
        )
    return _execute_and_convert(query)

def create(values):
    engine = chryso.connection.get()

    values['source'] = sqlalchemy.select([
        vanth.tables.OFXSource.c.uuid
    ]).where(vanth.tables.OFXSource.c.name == values.pop('institution'))

    values['uuid'] = uuid.uuid4()
    statement = vanth.tables.OFXAccount.insert().values(**values) # pylint: disable=no-value-for-parameter
    engine.execute(statement)
    return values['uuid']

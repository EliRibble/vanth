import uuid

import chryso.connection
import chryso.queryadapter
import passlib.apps
import sepiida.routing

import vanth.tables


def _to_dict(result):
    return {
       'username'   : result[vanth.tables.User.c.username],
       'password'   : result[vanth.tables.User.c.password],
       'name'       : result[vanth.tables.User.c.name],
       'uri'        : sepiida.routing.uri('user', result[vanth.tables.User.c.uuid]),
   }

def by_filter(filters):
    engine = chryso.connection.get()

    query = vanth.tables.User.select()
    query = chryso.queryadapter.map_and_filter(vanth.tables.User, filters, query)
    results = engine.execute(query).fetchall()
    return [_to_dict(result) for result in results]

def by_credentials(username, password):
    engine = chryso.connection.get()

    query = vanth.tables.User.select().where(vanth.tables.User.c.username == username)
    result = engine.execute(query).first()

    if not (result and passlib.apps.custom_app_context.verify(password, result[vanth.tables.User.c.password])):
        return None

    return _to_dict(result)

def create(name, username, password):
    engine = chryso.connection.get()

    _uuid = uuid.uuid4()
    statement = vanth.tables.User.insert().values( #pylint: disable=no-value-for-parameter
        name            = name,
        password        = passlib.apps.custom_app_context.encrypt(password),
        username        = username,
        uuid            = str(_uuid),
    )
    engine.execute(statement)

    return sepiida.routing.uri('user', _uuid)

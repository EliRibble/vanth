import uuid

import chryso.connection
import chryso.queryadapter
import passlib.apps
import sepiida.routing

import vanth.tables


def by_filter(filters):
    engine = chryso.connection.get()

    query = vanth.tables.User.select()
    query = chryso.queryadapter.map_and_filter(vanth.tables.User, filters, query)
    results = engine.execute(query).fetchall()
    return [{
       'username'   : result[vanth.tables.User.c.username],
       'password'   : result[vanth.tables.User.c.password],
       'name'       : result[vanth.tables.User.c.name],
   } for result in results]

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

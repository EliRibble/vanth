import logging
import uuid

import chryso.connection
import chryso.queryadapter
import passlib.apps
import sepiida.routing

import vanth.tables

LOGGER = logging.getLogger(__name__)

class User():
    def __init__(self, _uuid, name, username):
        self.uuid     = _uuid
        self.name     = name
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return str(self.uuid)

def load(user_id):
    engine = chryso.connection.get()

    query = vanth.tables.User.select().where(vanth.tables.User.c.uuid == str(user_id))
    results = engine.execute(query).fetchall()
    assert len(results) <= 1
    if not results:
        return None
    user = results[0]
    return User(
        _uuid    = user[vanth.tables.User.c.uuid],
        name     = user[vanth.tables.User.c.name],
        username = user[vanth.tables.User.c.username],
    )

def _to_dict(result):
    return {
       'name'       : result[vanth.tables.User.c.name],
       'username'   : result[vanth.tables.User.c.username],
       'uuid'       : result[vanth.tables.User.c.uuid],
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

    return User(
        _uuid    = result['uuid'],
        name     = result['name'],
        username = result['username'],
    )

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

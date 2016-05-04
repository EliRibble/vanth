import uuid

import chryso.connection
import passlib.apps
import sepiida.routing

import vanth.tables


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

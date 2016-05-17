import json
import uuid

import flask
import sepiida.routing

import vanth.platform.user

PUBLIC_ENDPOINTS = [
    'session.get',
    'session.post',
    'about.get',
]

def register_auth_handlers(app):
    app.before_request(require_user)

def endpoint():
    if flask.request.endpoint and flask.request.method:
        return "{}.{}".format(flask.request.endpoint.lower(), flask.request.method.lower())

def error(code, title, status_code=403):
    content = {
        'errors'    : [{
            'code'  : code,
            'title' : title,
        }]
    }
    return flask.make_response(json.dumps(content), status_code)

def require_user():
    user = None
    if flask.request.method == 'OPTIONS' and 'Access-Control-Request-Method' in flask.request.headers:
        return

    if not endpoint():
        return error('resource-not-found', 'The resource at URL {} could not be found'.format(flask.request.url), 404)

    if 'user_uri' not in flask.session:
        if endpoint() in PUBLIC_ENDPOINTS:
            return
        return error('unauthorized', 'You must provide a valid session cookie', 403)

    _, params = sepiida.routing.extract_parameters(flask.current_app, 'GET', flask.session['user_uri'])
    user = vanth.platform.user.by_filter({'uuid': [str(params['uuid'])]})
    if not user and endpoint() not in PUBLIC_ENDPOINTS:
        return error('invalid-user', 'The user tied to your session does not exist. Figure that out', 403)

    flask.g.current_user = user[0]
    flask.g.session = sepiida.routing.uri('session', flask.session['uuid'])

def current_user():
    return getattr(flask.g, 'current_user', None)

def is_authenticated():
    return current_user() is not None

def set_session(user):
    flask.session['user_uri'] = user['uri']
    flask.session['uuid'] = str(uuid.uuid4())

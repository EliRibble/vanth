import logging

import flask
import flask_login

import vanth.platform.user

LOGGER = logging.getLogger(__name__)
blueprint = flask.Blueprint('auth', __name__)

def load_user(user_id):
    LOGGER.debug("Loading user %s", user_id)
    return vanth.platform.user.load(user_id)

@blueprint.route('/login/', methods=['GET', 'POST', 'DELETE'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    elif flask.request.method == 'POST':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')
        LOGGER.debug("Checking credentials for %s %s", username, password)
        user = vanth.platform.user.by_credentials(username, password)
        if not user:
            return flask.make_response('error', 403)
        flask_login.login_user(user)
    elif flask.request.method == 'DELETE':
        flask_login.logout_user()
    return flask.redirect('/')

@blueprint.route('/logout/', methods=['POST'])
def logout():
    LOGGER.info("Logging out user %s", flask.session['user_id'])
    flask_login.logout_user()
    return flask.redirect('/login/')

def require_login():
    LOGGER.debug("Current user %s", flask.session.get('user_id'))
    if flask.request.path == '/login/':
        return
    if not flask.session.get('user_id'):
        return flask.redirect('/login/')

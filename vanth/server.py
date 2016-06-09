import logging

import flask
import flask_login
import flask_uuid
import sepiida.cors
import sepiida.endpoints

import vanth.api.about
import vanth.api.ofxsource
import vanth.api.session
import vanth.api.user
import vanth.auth
import vanth.platform.user

LOGGER = logging.getLogger(__name__)

EXPOSE_HEADERS = [
    'Location',
]

def index():
    return flask.render_template('index.html')

def load_user(user_id):
    LOGGER.debug("Loading user %s", user_id)
    return vanth.platform.user.load(user_id)

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

def logout():
    LOGGER.info("Logging out user %s", flask.session['user_id'])
    flask_login.logout_user()
    return flask.redirect('/login/')

def require_login():
    LOGGER.debug("Current user %s for %s", flask.session, flask.request.path)
    if flask.request.path == '/login/':
        return
    if not flask.session.get('user_id'):
        return flask.redirect('/login/')

def create_app(config):
    app = flask.Flask('vanth', template_folder='../templates')

    flask_uuid.FlaskUUID(app)
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    login_manager.user_loader(load_user)

    app.config.update(
        API_TOKEN                 = config.api_token,
        DEBUG                     = config.debug,
        SECRET_KEY                = config.secret_key,
        SESSION_COOKIE_DOMAIN     = config.session_cookie_domain,
    )
    sepiida.cors.register_cors_handlers(
        app,
        domains=['localhost:8080', 'www.vanth.com'],
        supports_credentials=True,
        expose_headers=EXPOSE_HEADERS,
    )
    #vanth.auth.register_auth_handlers(app)

    app.route('/',          methods=['GET'])(index)
    app.route('/login/',    methods=['GET', 'POST', 'DELETE'])(login)
    app.route('/logout/',   methods=['POST'])(logout)

    app.before_request(require_login)

    sepiida.endpoints.add_resource(app, vanth.api.about.About,          endpoint='about')
    sepiida.endpoints.add_resource(app, vanth.api.ofxsource.OFXSource,  endpoint='ofxsource')
    sepiida.endpoints.add_resource(app, vanth.api.session.Session,      endpoint='session')
    sepiida.endpoints.add_resource(app, vanth.api.user.User,            endpoint='user')

    return app

import uuid

import flask
import flask_login
import flask_uuid
import sepiida.endpoints

import vanth.api.about
import vanth.user


def index():
    return flask.render_template('index.html')

def load_user(user_id):
    return vanth.user.load(user_id)

def login():
    if flask.request.method == 'GET':
        return flask.render_template('index.html')
    elif flask.request.method == 'POST':
        user = vanth.user.load(uuid.uuid4())
        flask_login.login_user(user)
    elif flask.request.method == 'DELETE':
        flask_login.logout_user()
    return flask.redirect('/')

def logout():
    flask_login.logout_user()
    return flask.redirect('/')

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

    app.route('/', methods=['GET'])(index)
    app.route('/login/', methods=['GET', 'POST', 'DELETE'])(login)
    app.route('/logout/', methods=['POST'])(logout)

    sepiida.endpoints.add_resource(app, vanth.api.about.About, endpoint='about')

    return app

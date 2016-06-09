import logging

import flask
import flask_login
import flask_uuid

import vanth.auth
import vanth.pages.accounts
import vanth.pages.index

LOGGER = logging.getLogger(__name__)

EXPOSE_HEADERS = [
    'Location',
]

def create_app(config):
    app = flask.Flask('vanth', template_folder='../templates')

    flask_uuid.FlaskUUID(app)
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    login_manager.user_loader(vanth.auth.load_user)

    app.config.update(
        API_TOKEN                 = config.api_token,
        DEBUG                     = config.debug,
        SECRET_KEY                = config.secret_key,
        SESSION_COOKIE_DOMAIN     = config.session_cookie_domain,
    )

    app.register_blueprint(vanth.pages.accounts.blueprint)
    app.register_blueprint(vanth.pages.index.blueprint)
    app.register_blueprint(vanth.auth.blueprint)

    app.before_request(vanth.auth.require_login)


    LOGGER.debug("app created")
    return app

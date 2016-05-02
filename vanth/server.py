from flask import Flask
from flask_uuid import FlaskUUID
from sepiida import endpoints

import vanth.api.about


def create_app(config):
    app = Flask('vanth')

    FlaskUUID(app)
    app.config.update(
        API_TOKEN                 = config.api_token,
        DEBUG                     = config.debug,
        SECRET_KEY                = config.secret_key,
        SESSION_COOKIE_DOMAIN     = config.session_cookie_domain,
    )

    endpoints.add_resource(app, vanth.api.about.About,               endpoint='about')

    return app

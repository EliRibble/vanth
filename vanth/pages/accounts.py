import flask

blueprint = flask.Blueprint('accounts', __name__)

@blueprint.route('/accounts/')
def accounts():
    my_accounts = []
    return flask.render_template('accounts.html', accounts=my_accounts)

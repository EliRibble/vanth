import flask

import vanth.celery
import vanth.pages.tools
import vanth.platform.ofxaccount
import vanth.platform.ofxsource

blueprint = flask.Blueprint('accounts', __name__)

@blueprint.route('/accounts/', methods=['GET'])
def get_accounts():
    my_accounts = vanth.platform.ofxaccount.by_user(flask.session['user_id'])
    sources = vanth.platform.ofxsource.get()
    return flask.render_template('accounts.html', accounts=my_accounts, sources=sources)

@blueprint.route('/accounts/<uuid:account_uuid>/', methods=['GET'])
def get_account(account_uuid):
    account = vanth.platform.ofxaccount.by_uuid(account_uuid)
    records = vanth.platform.ofxrecord.by_account(account_uuid)
    return flask.render_template('account.html', account=account, records=records)

@blueprint.route('/account/', methods=['POST'])
@vanth.pages.tools.parse({
    'account_id'    : str,
    'account_type'  : str,
    'institution'   : str,
    'name'          : str,
    'password'      : str,
    'user_id'       : str,
})
def post_account(arguments):
    arguments['owner'] = flask.session['user_id']
    vanth.platform.ofxaccount.create(arguments)
    return flask.redirect('/accounts/')

@blueprint.route('/update/', methods=['POST'])
@vanth.pages.tools.parse({
    'account_uuid'  : str,
})
def post_update(arguments):
    vanth.celery.update_account.delay(**arguments)
    return flask.redirect('/accounts/')

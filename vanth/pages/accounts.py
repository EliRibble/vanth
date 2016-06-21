import flask

import vanth.platform.ofxaccount
import vanth.platform.ofxsource

blueprint = flask.Blueprint('accounts', __name__)

@blueprint.route('/accounts/', methods=['GET'])
def get_accounts():
    my_accounts = vanth.platform.ofxaccount.get(flask.session['user_id'])
    sources = vanth.platform.ofxsource.get()
    return flask.render_template('accounts.html', accounts=my_accounts, sources=sources)

@blueprint.route('/account/', methods=['POST'])
def post_account():
    account_type = flask.request.form.get('account_type')
    institution  = flask.request.form.get('institution')
    name         = flask.request.form.get('name')
    password     = flask.request.form.get('password')
    userid       = flask.request.form.get('userid')


    vanth.platform.ofxaccount.create(flask.session['user_id'], name, account_type, institution, password, userid)
    return flask.redirect('/accounts/')

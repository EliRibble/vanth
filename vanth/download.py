import requests

import vanth.ofx
import vanth.platform.ofxaccount


def do_all():
    sources = {source['name']: source for source in vanth.platform.ofxsource.get()}
    accounts = vanth.platform.ofxaccount.by_user(user_id=None)
    for account in accounts:
        transactions(sources[account['institution']], account)

def transactions(source, account):
    body = vanth.ofx.query_transactions(source, account)
    response = requests.post('https://ofx.americafirst.com/', data=body, headers={'Content-Type': 'application/x-ofx'})
    assert response.ok, response.text
    return vanth.ofx.parse(response.text)

import celery

import vanth.download
import vanth.main
import vanth.platform.ofxaccount
import vanth.platform.ofxrecord
import vanth.platform.ofxsource

app = celery.Celery('vanth')
app.conf.CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
app.conf.CELERY_TASK_SERIALIZER = 'json'
app.conf.CELERY_ALWAYS_EAGER = True

@app.task()
def update_account(account_uuid):
    account = vanth.platform.ofxaccount.by_uuid(account_uuid)[0]
    source = vanth.platform.ofxsource.by_uuid(account['source']['uuid'])[0]
    document = vanth.download.transactions(source, account)
    vanth.platform.ofxrecord.ensure_exists(account, document.body.statement.transactions.items)

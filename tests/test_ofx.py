import datetime

import vanth.ofx


def MST():
    return datetime.timezone(datetime.timedelta(hours=-7), 'MST')

def MDT():
    return datetime.timezone(datetime.timedelta(hours=-6), 'MDT')

def test_query_transactions(mocker):
    institution = {
        'bankid'    : "1234567",
        'fid'       : "12345",
        'name'      : "AFCU",
    }
    account = {
        "account_id"    : "123456-0.9:CHK",
        "user_id"       : "123456789",
        "password"      : "1234",
        "type"          : "checking",
    }
    with mocker.patch('vanth.ofx.now', return_value='20160102030405.000[-7:MST]'):
        results = vanth.ofx.query_transactions(institution, account, start=datetime.date(2016, 1, 2))
    with open('tests/files/query_transactions.ofx', 'rb') as f:
        expected = f.read().decode('utf-8')
    assert results == expected

def test_parse():
    with open('tests/files/transactions.ofx', 'rb') as f:
        transactions = f.read().decode('utf-8')
    document = vanth.ofx.parse(transactions)
    assert document.header == {
        'CHARSET'       : '1252',
        'COMPRESSION'   : 'NONE',
        'DATA'          : 'OFXSGML',
        'ENCODING'      : 'USASCII',
        'NEWFILEUID'    : 'NONE',
        'OFXHEADER'     : '100',
        'OLDFILEUID'    : 'NONE',
        'SECURITY'      : 'NONE',
        'VERSION'       : '102'
    }
    assert document.body.status.code == '0'
    assert document.body.status.severity == 'INFO'
    assert document.body.status.message == 'The operation succeeded.'
    assert document.body.statement.status.code == '0'
    assert document.body.statement.status.severity == 'INFO'
    assert document.body.statement.status.message is None
    assert document.body.statement.transactions.currency == 'USD'
    assert document.body.statement.transactions.account.accountid == '123456-0.9:CHK'
    assert document.body.statement.transactions.account.bankid == '324377516'
    assert document.body.statement.transactions.account.type == 'CHECKING'
    assert document.body.statement.transactions.start == datetime.datetime(2015, 12, 31, 17, 0, tzinfo=MST())
    assert document.body.statement.transactions.end == datetime.datetime(2016, 6, 22, 11, 12, 42, tzinfo=MDT())
    expected_items = [{
        'amount'    : -50.19,
        'available' : datetime.datetime(2015, 12, 31, 12),
        'id'        : '0006547',
        'memo'      : 'POINT OF SALE PURCHASE #0006547',
        'name'      : 'UT LEHI COSTCO WHSE #0733',
        'posted'    : datetime.datetime(2015, 12, 31, 12),
        'type'      : 'POS',
    },{
        'amount'    : -79.64,
        'available' : datetime.datetime(2015, 12, 31, 12),
        'id'        : '0006548',
        'memo'      : '#0006548',
        'name'      : 'Payment to PACIFICORP ONLIN',
        'posted'    : datetime.datetime(2015, 12, 31, 12),
        'type'      : 'PAYMENT',
    },{
        'amount'    : 0.84,
        'available' : datetime.datetime(2015, 12, 31, 12),
        'id'        : '0006549',
        'memo'      : 'ANNUAL PERCENTAGE YIELD EARNED IS   .05% #0006549',
        'name'      : 'DIVIDEND FOR 12/01/15 - 12/31/1',
        'posted'    : datetime.datetime(2015, 12, 31, 12),
        'type'      : 'INT',
    }]
    items = [dict(item) for item in document.body.statement.transactions.items]
    assert items == expected_items

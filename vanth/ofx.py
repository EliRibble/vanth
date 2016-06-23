import collections
import datetime
import re

import vanth.sgml

Document = collections.namedtuple('Document', ['header', 'body'])

class Body(): # pylint:disable=too-few-public-methods
    def __init__(self, sgml):
        self.status = Status(sgml['SIGNONMSGSRSV1']['SONRS']['STATUS'])
        self.statement = TransactionStatement(sgml['BANKMSGSRSV1']['STMTTRNRS'])

class Status(): # pylint:disable=too-few-public-methods
    def __init__(self, sgml):
        self.code = sgml['CODE'].value
        self.severity = sgml['SEVERITY'].value
        self.message = sgml['MESSAGE'].value if sgml['MESSAGE'] else None

class TransactionStatement(): # pylint:disable=too-few-public-methods
    def __init__(self, sgml):
        self.trnuid = sgml['TRNUID'].value
        self.status = Status(sgml['STATUS'])
        self.transactions = TransactionList(sgml['STMTRS'])

class TransactionList(): # pylint:disable=too-few-public-methods
    def __init__(self, sgml):
        self.currency = sgml['CURDEF'].value
        self.account = Account(sgml['BANKACCTFROM'])
        self.start = _parse_date_with_tz(sgml['BANKTRANLIST']['DTSTART'].value)
        self.end = _parse_date_with_tz(sgml['BANKTRANLIST']['DTEND'].value)
        self.items = [Transaction(child) for child in sgml['BANKTRANLIST'].children if child.name == 'STMTTRN']

class Transaction(): # pylint:disable=too-few-public-methods
    def __init__(self, sgml):
        self.amount    = float(sgml['TRNAMT'].value)
        self.available = _parse_date(sgml['DTAVAIL'].value)
        self.id        = sgml['FITID'].value
        self.memo      = sgml['MEMO'].value
        self.name      = sgml['NAME'].value
        self.posted    = _parse_date(sgml['DTPOSTED'].value)
        self.type      = sgml['TRNTYPE'].value

    def __iter__(self):
        return ((prop, getattr(self, prop)) for prop in ('amount', 'available', 'id', 'memo', 'name', 'posted', 'type'))

class Account(): # pylint:disable=too-few-public-methods
    def __init__(self, sgml):
        self.bankid = sgml['BANKID'].value
        self.accountid = sgml['ACCTID'].value
        self.type = sgml['ACCTTYPE'].value

def _fix_offset(offset):
    result = int(offset) * 100
    return "{:04d}".format(result) if result > 0 else "{:05d}".format(result)

def _parse_date(date):
    return datetime.datetime.strptime(date, "%Y%m%d%H%M%S.000")

def _parse_date_with_tz(date):
    match = re.match(r'(?P<datetime>\d+)\.\d+\[(?P<offset>[\d\-]+):(?P<tzname>\w+)\]', date)
    if not match:
        raise ValueError("Unable to extract datetime from {}".format(date))
    formatted = "{datetime} {offset} {tzname}".format(
        datetime = match.group('datetime'),
        offset = _fix_offset(match.group('offset')),
        tzname = match.group('tzname'),
    )
    return datetime.datetime.strptime(formatted, "%Y%m%d%H%M%S %z %Z")

def header():
    return "\r\n".join([
        "OFXHEADER:100",
        "DATA:OFXSGML",
        "VERSION:102",
        "SECURITY:NONE",
        "ENCODING:USASCII",
        "CHARSET:1252",
        "COMPRESSION:NONE",
        "OLDFILEUID:NONE",
        "NEWFILEUID:NONE",
    ])

def now():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S.000[-7:MST]")

def signonmsg(institution, account):
    return "\r\n".join([
        "<SIGNONMSGSRQV1>",
            "<SONRQ>",
                "<DTCLIENT>{}".format(now()),
                "<USERID>{}".format(account['user_id']),
                "<USERPASS>{}".format(account['password']),
                "<LANGUAGE>ENG",
                "<FI>",
                    "<ORG>{}".format(institution['name']),
                    "<FID>{}".format(institution['fid']),
                "</FI>",
                "<APPID>QWIN",
                "<APPVER>1200",
            "</SONRQ>",
        "</SIGNONMSGSRQV1>",
    ])

def bankmsg(institution, account, start):
    return "\r\n".join([
        "<BANKMSGSRQV1>",
            "<STMTTRNRQ>",
                "<TRNUID>00000000",
                "<STMTRQ>",
                    "<BANKACCTFROM>",
                        "<BANKID>{}".format(institution['bankid']),
                        "<ACCTID>{}".format(account['account_id']),
                        "<ACCTTYPE>{}".format(account['type'].upper()),
                    "</BANKACCTFROM>",
                    "<INCTRAN>",
                        "<DTSTART>{}".format(start.strftime("%Y%m%d")),
                        "<INCLUDE>Y",
                    "</INCTRAN>",
                "</STMTRQ>",
            "</STMTTRNRQ>",
        "</BANKMSGSRQV1>",
    ])

def body(institution, account, start):
    return "<OFX>\r\n" + signonmsg(institution, account) + "\r\n" + bankmsg(institution, account, start) + "\r\n</OFX>"

def query_transactions(institution, account, start=None):
    start = start or datetime.datetime.now() - datetime.timedelta(days=14)
    return header() + (2*"\r\n") + body(institution, account, start) + "\r\n"


def _first_empty_line(lines):
    for i, line in enumerate(lines):
        if not line:
            return i

def _parse_header(header_lines):
    splits = [line.partition(':') for line in header_lines]
    return {k: v for k, _, v in splits}

def parse(content):
    lines = content.split('\r\n')
    split = _first_empty_line(lines)
    header_lines = lines[:split]
    _header = _parse_header(header_lines)
    _body = vanth.sgml.parse('\n'.join(lines[split+1:]))
    return Document(_header, Body(_body))

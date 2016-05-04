import chryso.constants
from sqlalchemy import (Column, Date, DateTime, Float, ForeignKey, Integer,
                        MetaData, String, Table, func)
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData(naming_convention=chryso.constants.CONVENTION)

User = Table('users', metadata,
    Column('uuid',          UUID(), primary_key=True),
    Column('username',      String(255), nullable=False),
    Column('name',          String(255), nullable=False),
    Column('company',       String(255), nullable=True),
    Column('password',      String(128), nullable=False),
    Column('created_at',    DateTime,    nullable=False, server_default=func.now()),
    Column('updated_at',    DateTime,    nullable=False, server_default=func.now(), onupdate=func.now()),
    Column('deleted_at',    DateTime,    nullable=True),
)

CreditCard = Table('credit_card', metadata,
    Column('uuid',              UUID(as_uuid=True),         primary_key=True),
    Column('brand',             String(20),     nullable=False), # The brand of the card, like 'visa'
    Column('card_id',           String(100),    nullable=False), # The ID of the card from Stripe
    Column('country',           String(1024),   nullable=False), # The Country of the card, like 'US'
    Column('cvc_check',         String(100),    nullable=False), # The CVC value from Stripe, like 'unchecked'
    Column('expiration_month',  Integer(),      nullable=False), # The month the card expires
    Column('expiration_year',   Integer(),      nullable=False), # The year the card expires
    Column('last_four',         Integer(),      nullable=False), # The last four digits of the card
    Column('token',             String(),       nullable=False), # The token we can use with Stripe to do stuff
    Column('user_uri',          String(2048),   nullable=False), # The URI of the user that created the record
    Column('created',           DateTime(),     nullable=False, server_default=func.now()),
    Column('updated',           DateTime(),     nullable=False, server_default=func.now(), onupdate=func.now()),
    Column('deleted',           DateTime(),     nullable=True),
)

OFXSource = Table('ofxsource',  metadata,
    Column('uuid',              UUID(as_uuid=True),         primary_key=True),
    Column('name',              String(255),     nullable=False), # The name of the institution such as 'America First Credit Union'
    Column('fid',               String(255),     nullable=False), # The FID of the institution, such as 54324
    Column('bankid',            String(255),     nullable=False), # The bank ID of the institution such as 324377516
    Column('created',           DateTime(),      nullable=False, server_default=func.now()),
    Column('updated',           DateTime(),     nullable=False, server_default=func.now(), onupdate=func.now()),
)

OFXAccount = Table('ofxaccount', metadata,
    Column('uuid',              UUID(as_uuid=True),  primary_key=True),
    Column('user_id',           String(255),         nullable=False), # The user ID for the bank
    Column('password',          String(255),         nullable=False), # The encrypted password for the account
    Column('type',              String(255),         nullable=False), # The account type, like 'checking'
    Column('source',            None,                ForeignKey(OFXSource.c.uuid, name='fk_ofxsource'), nullable=False),
    Column('created',           DateTime(),          nullable=False, server_default=func.now()),
    Column('updated',           DateTime(),     nullable=False, server_default=func.now(), onupdate=func.now()),
)

OFXRecord = Table('ofxrecord',  metadata,
    Column('uuid',              UUID(as_uuid=True),         primary_key=True),
    Column('fid',               String(255),    nullable=False), # The Financial institution's ID
    Column('amount',            Float(),        nullable=False), # The amount of the record, like -177.91
    Column('available',         Date(),         nullable=True), # The date the record was available
    Column('name',              String(1024),   nullable=False), # The name of the record, like 'UT SLC SAMSCLUB #4719'
    Column('posted',            Date(),         nullable=True), # The date the record posted
    Column('memo',              String(2048),   nullable=True), # The memo of the transaction, like 'POINT OF SALE PURCHASE #0005727'
    Column('type',              String(255),    nullable=True), # The type of the record, like 'POS'
    Column('created',           DateTime(),     nullable=False, server_default=func.now()),
    Column('updated',           DateTime(),     nullable=False, server_default=func.now(), onupdate=func.now()),
)

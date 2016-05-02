"""create initial tables

Revision ID: 58ea73d3d07b
Revises: 
Create Date: 2016-05-02 08:42:38.061749

"""

# revision identifiers, used by Alembic.
revision = '58ea73d3d07b'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('credit_card',
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('brand', sa.String(length=20), nullable=False),
        sa.Column('card_id', sa.String(length=100), nullable=False),
        sa.Column('country', sa.String(length=1024), nullable=False),
        sa.Column('cvc_check', sa.String(length=100), nullable=False),
        sa.Column('expiration_month', sa.Integer(), nullable=False),
        sa.Column('expiration_year', sa.Integer(), nullable=False),
        sa.Column('last_four', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('user_uri', sa.String(length=2048), nullable=False),
        sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('uuid', name=op.f('pk_credit_card'))
    )
    op.create_table('ofxrecord',
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('fid', sa.String(length=255), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('available', sa.Date(), nullable=True),
        sa.Column('name', sa.String(length=1024), nullable=False),
        sa.Column('posted', sa.Date(), nullable=True),
        sa.Column('memo', sa.String(length=2048), nullable=True),
        sa.Column('type', sa.String(length=255), nullable=True),
        sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('uuid', name=op.f('pk_ofxrecord'))
    )
    op.create_table('ofxsource',
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('fid', sa.String(length=255), nullable=False),
        sa.Column('bankid', sa.String(length=255), nullable=False),
        sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('uuid', name=op.f('pk_ofxsource'))
    )
    op.create_table('ofxaccount',
    )


def downgrade():
    op.drop_table('ofxaccount')
    op.drop_table('ofxsource')
    op.drop_table('ofxrecord')
    op.drop_table('credit_card')

"""add ofxupdate

Revision ID: 00f2b77f1d2c
Revises: ab038e16ec9a
Create Date: 2016-06-28 15:48:14.994815

"""

# revision identifiers, used by Alembic.
revision = '00f2b77f1d2c'
down_revision = 'ab038e16ec9a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('ofxupdate',
        sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.Column('ofxaccount', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['ofxaccount'], ['ofxaccount.uuid'], name='fk_ofxaccount'),
        sa.PrimaryKeyConstraint('uuid', name=op.f('pk_ofxupdate'))
    )


def downgrade():
    op.drop_table('ofxupdate')

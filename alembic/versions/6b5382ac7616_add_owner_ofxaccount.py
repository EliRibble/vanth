"""add owner ofxaccount

Revision ID: 6b5382ac7616
Revises: 4990a9f1ada3
Create Date: 2016-06-21 07:12:22.486560

"""

# revision identifiers, used by Alembic.
revision = '6b5382ac7616'
down_revision = '4990a9f1ada3'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column('ofxaccount', sa.Column('owner', postgresql.UUID(), nullable=False))
    op.create_foreign_key('fk_user', 'ofxaccount', 'users', ['owner'], ['uuid'])


def downgrade():
    op.drop_constraint('fk_user', 'ofxaccount', type_='foreignkey')
    op.drop_column('ofxaccount', 'owner')

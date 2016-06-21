"""add ofxaccount t name

Revision ID: d68c4fbb811f
Revises: 6b5382ac7616
Create Date: 2016-06-21 07:27:00.754391

"""

# revision identifiers, used by Alembic.
revision = 'd68c4fbb811f'
down_revision = '6b5382ac7616'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('ofxaccount', sa.Column('name', sa.String(length=255), nullable=False))


def downgrade():
    op.drop_column('ofxaccount', 'name')

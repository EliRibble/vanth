"""standardize_columns

Revision ID: ab038e16ec9a
Revises: 4b8ce290f890
Create Date: 2016-06-28 15:44:52.141256

"""

# revision identifiers, used by Alembic.
revision = 'ab038e16ec9a'
down_revision = '4b8ce290f890'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('ofxaccount', sa.Column('deleted', sa.DateTime(), nullable=True))
    op.add_column('ofxrecord', sa.Column('deleted', sa.DateTime(), nullable=True))
    op.add_column('ofxsource', sa.Column('deleted', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('ofxsource', 'deleted')
    op.drop_column('ofxrecord', 'deleted')
    op.drop_column('ofxaccount', 'deleted')

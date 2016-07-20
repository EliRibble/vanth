"""ofxsource_fid_nonunique

Revision ID: 16ac2bbf8b81
Revises: 3ec1289eae7a
Create Date: 2016-07-20 15:41:03.117666

"""

# revision identifiers, used by Alembic.
revision = '16ac2bbf8b81'
down_revision = '3ec1289eae7a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.drop_constraint('uq_ofxsource_fid', 'ofxsource', type_='unique')


def downgrade():
    op.create_unique_constraint('uq_ofxsource_fid', 'ofxsource', ['fid'])

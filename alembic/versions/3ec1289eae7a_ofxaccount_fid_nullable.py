"""ofxaccount_fid_nullable

Revision ID: 3ec1289eae7a
Revises: 3bac184298c9
Create Date: 2016-07-20 15:36:28.157723

"""

# revision identifiers, used by Alembic.
revision = '3ec1289eae7a'
down_revision = '3bac184298c9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.alter_column('ofxsource', 'fid',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)


def downgrade():
    op.alter_column('ofxsource', 'fid',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)

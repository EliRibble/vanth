"""ofxsource_url

Revision ID: a5eaf1296414
Revises: eac3a08698a7
Create Date: 2016-07-20 15:23:45.880556

"""

# revision identifiers, used by Alembic.
revision = 'a5eaf1296414'
down_revision = 'eac3a08698a7'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column('ofxsource', sa.Column('url', sa.String(length=4096), nullable=False))


def downgrade():
    op.drop_column('ofxsource', 'url')

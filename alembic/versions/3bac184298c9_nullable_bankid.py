"""nullable_bankid

Revision ID: 3bac184298c9
Revises: a5eaf1296414
Create Date: 2016-07-20 15:33:20.377382

"""

# revision identifiers, used by Alembic.
revision = '3bac184298c9'
down_revision = 'a5eaf1296414'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.alter_column('ofxsource', 'bankid',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)


def downgrade():
    op.alter_column('ofxsource', 'bankid',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)

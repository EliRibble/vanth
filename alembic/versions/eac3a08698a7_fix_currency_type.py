"""fix currency type

Revision ID: eac3a08698a7
Revises: 00f2b77f1d2c
Create Date: 2016-07-01 11:54:56.272364

"""

# revision identifiers, used by Alembic.
revision = 'eac3a08698a7'
down_revision = '00f2b77f1d2c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    if not op.get_context().as_sql:
        connection = op.get_bind()
        connection.execution_options(isolation_level='AUTOCOMMIT')

    op.execute('ALTER TABLE ofxrecord ALTER COLUMN amount TYPE NUMERIC(20, 2) USING amount::numeric;')

def downgrade():
    pass

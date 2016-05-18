"""add unique constraints

Revision ID: 4990a9f1ada3
Revises: 688af5ecd407
Create Date: 2016-05-18 15:40:33.511871

"""

# revision identifiers, used by Alembic.
revision = '4990a9f1ada3'
down_revision = '688af5ecd407'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_unique_constraint('uq_credit_card_id', 'credit_card', ['card_id'])
    op.create_unique_constraint('uq_ofxsource_fid', 'ofxsource', ['fid'])
    op.create_unique_constraint('uq_user_username', 'users', ['username'])


def downgrade():
    op.drop_constraint('uq_user_username', 'users', type_='unique')
    op.drop_constraint('uq_ofxsource_fid', 'ofxsource', type_='unique')
    op.drop_constraint('uq_credit_card_id', 'credit_card', type_='unique')

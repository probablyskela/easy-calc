"""empty message

Revision ID: 18acc04e566b
Revises: faaf03ce2abf
Create Date: 2022-10-16 16:24:56.326773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18acc04e566b'
down_revision = 'faaf03ce2abf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'calculators', ['code'])
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'calculators', type_='unique')
    # ### end Alembic commands ###

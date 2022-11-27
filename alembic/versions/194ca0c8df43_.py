"""empty message

Revision ID: 194ca0c8df43
Revises: 4800f27bceed
Create Date: 2022-11-27 23:16:01.469262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '194ca0c8df43'
down_revision = '4800f27bceed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('calculators', sa.Column('input', sa.String(length=256), nullable=False))
    op.drop_column('calculators', 'input_data')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('calculators', sa.Column('input_data', sa.VARCHAR(length=256), autoincrement=False, nullable=False))
    op.drop_column('calculators', 'input')
    # ### end Alembic commands ###

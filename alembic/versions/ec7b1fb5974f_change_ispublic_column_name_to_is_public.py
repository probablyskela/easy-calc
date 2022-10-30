"""Change isPublic column name to is_public

Revision ID: ec7b1fb5974f
Revises: ec12b2ba3282
Create Date: 2022-10-29 15:11:59.962113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec7b1fb5974f'
down_revision = 'ec12b2ba3282'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('calculators', sa.Column('is_public', sa.Boolean(), nullable=False))
    op.drop_column('calculators', 'isPublic')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('calculators', sa.Column('isPublic', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('calculators', 'is_public')
    # ### end Alembic commands ###

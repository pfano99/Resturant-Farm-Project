"""empty message

Revision ID: d4a7ea3297eb
Revises: b953fc2dcc01
Create Date: 2021-05-20 13:52:16.600366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4a7ea3297eb'
down_revision = 'b953fc2dcc01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('stock_count', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'stock_count')
    # ### end Alembic commands ###

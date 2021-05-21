"""empty message

Revision ID: b953fc2dcc01
Revises: f5b756ab51b6
Create Date: 2021-05-20 12:33:41.747631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b953fc2dcc01'
down_revision = 'f5b756ab51b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('images_ibfk_1', 'images', type_='foreignkey')
    op.create_foreign_key(None, 'images', 'product', ['product_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'images', type_='foreignkey')
    op.create_foreign_key('images_ibfk_1', 'images', 'farmer', ['product_id'], ['id'])
    # ### end Alembic commands ###
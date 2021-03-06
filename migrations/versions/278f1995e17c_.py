"""empty message

Revision ID: 278f1995e17c
Revises: d4a7ea3297eb
Create Date: 2021-05-20 14:44:21.645989

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '278f1995e17c'
down_revision = 'd4a7ea3297eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('rest_client_id', sa.Integer(), nullable=True))
    op.add_column('cart', sa.Column('rest_seller_id', sa.Integer(), nullable=True))
    op.drop_constraint('cart_ibfk_3', 'cart', type_='foreignkey')
    op.drop_constraint('cart_ibfk_4', 'cart', type_='foreignkey')
    op.create_foreign_key(None, 'cart', 'restuarant', ['rest_client_id'], ['id'])
    op.create_foreign_key(None, 'cart', 'restuarant', ['rest_seller_id'], ['id'])
    op.drop_column('cart', 'comp_client_id')
    op.drop_column('cart', 'comp_seller_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('comp_seller_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('cart', sa.Column('comp_client_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.create_foreign_key('cart_ibfk_4', 'cart', 'restuarant', ['comp_seller_id'], ['id'])
    op.create_foreign_key('cart_ibfk_3', 'cart', 'restuarant', ['comp_client_id'], ['id'])
    op.drop_column('cart', 'rest_seller_id')
    op.drop_column('cart', 'rest_client_id')
    # ### end Alembic commands ###

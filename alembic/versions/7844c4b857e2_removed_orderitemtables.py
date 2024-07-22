"""removed orderitemtables

Revision ID: 7844c4b857e2
Revises: 48240f5734bd
Create Date: 2024-07-21 20:04:55.040184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7844c4b857e2'
down_revision: Union[str, None] = '48240f5734bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orderproductassociation',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], ),
    sa.PrimaryKeyConstraint('order_id', 'product_id')
    )
    op.drop_table('orderitems')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orderitems',
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('total_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('order_item_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], name='orderitems_order_id_fkey'),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], name='orderitems_product_id_fkey'),
    sa.PrimaryKeyConstraint('order_item_id', name='orderitems_pkey')
    )
    op.drop_table('orderproductassociation')
    # ### end Alembic commands ###
"""add users, pets, products, orders, orderitem, services, booking, petbookassoc tables

Revision ID: 34fc99a8dfbe
Revises: 
Create Date: 2024-07-19 05:51:17.261125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '34fc99a8dfbe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('product_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('services',
    sa.Column('service_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('service_id')
    )
    op.create_table('users',
    sa.Column('full_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('role', sa.Enum('ADMIN', 'BASIC', name='roles'), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('phone_number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('booking',
    sa.Column('date_and_time', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('reserved_date', sa.DateTime(), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['services.service_id'], ),
    sa.PrimaryKeyConstraint('booking_id')
    )
    op.create_table('orders',
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('pets',
    sa.Column('pet_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('DOG', 'CAT', 'BIRD', 'FISH', 'PIG', 'HAMSTER', 'HEDGEHOG', 'OTHERS', name='pettypes'), nullable=False),
    sa.Column('breed', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('pet_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('pet_id')
    )
    op.create_table('orderitems',
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('order_item_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], ),
    sa.PrimaryKeyConstraint('order_item_id')
    )
    op.create_table('petsbookingsassociation',
    sa.Column('pet_id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], ),
    sa.ForeignKeyConstraint(['pet_id'], ['pets.pet_id'], ),
    sa.PrimaryKeyConstraint('pet_id', 'booking_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('petsbookingsassociation')
    op.drop_table('orderitems')
    op.drop_table('pets')
    op.drop_table('orders')
    op.drop_table('booking')
    op.drop_table('users')
    op.drop_table('services')
    op.drop_table('products')
    # ### end Alembic commands ###

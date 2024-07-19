"""modified something

Revision ID: 48240f5734bd
Revises: 9b45a33b9802
Create Date: 2024-07-19 10:33:29.594007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '48240f5734bd'
down_revision: Union[str, None] = '9b45a33b9802'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bookingstate = sqlmodel.Enum("PENDING", "CONFIRMED", "CANCELLED", "COMPLETED", name="bookingstate")
    orderstate = sqlmodel.Enum("PENDING", "CONFIRMED", "CANCELLED", "COMPLETED", name="orderstate")
    bookingstate.create(op.get_bind(), checkfirst=True)
    orderstate.create(op.get_bind(), checkfirst=True)
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('status', sa.Enum('PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED', name='bookingstate'), nullable=True))
    op.add_column('orders', sa.Column('status', sa.Enum('PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED', name='orderstate'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'status')
    op.drop_column('booking', 'status')
    # ### end Alembic commands ###

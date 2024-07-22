"""add datetime columns into past tables with nullable false

Revision ID: 6ba0bb5107f3
Revises: b4971f3a9928
Create Date: 2024-07-22 11:41:46.169660

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6ba0bb5107f3'
down_revision: Union[str, None] = 'b4971f3a9928'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('booking', sa.Column('reserved_date', postgresql.TIMESTAMP(), nullable=False, server_default=sa.func.current_timestamp()))
    op.add_column('orders', sa.Column('order_date', postgresql.TIMESTAMP(), nullable=False, server_default=sa.func.current_timestamp()))
    op.add_column('products', sa.Column('last_updated', postgresql.TIMESTAMP(), nullable=False, server_default=sa.func.current_timestamp()))



def downgrade() -> None:
    op.drop_column('products', 'last_updated')
    op.drop_column('orders', 'order_date')
    op.drop_column('booking', 'reserved_date')

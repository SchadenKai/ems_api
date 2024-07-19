"""nmake products name unique

Revision ID: 9b45a33b9802
Revises: c325848d189c
Create Date: 2024-07-19 08:18:00.697997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '9b45a33b9802'
down_revision: Union[str, None] = 'c325848d189c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'products', ['product_name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='unique')
    # ### end Alembic commands ###
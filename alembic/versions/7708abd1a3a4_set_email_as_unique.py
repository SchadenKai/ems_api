"""set email as unique

Revision ID: 7708abd1a3a4
Revises: b6fe64c69f97
Create Date: 2024-07-28 19:30:20.554208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7708abd1a3a4'
down_revision: Union[str, None] = 'b6fe64c69f97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('products', 'photo_url',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.alter_column('products', 'photo_url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('products', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###

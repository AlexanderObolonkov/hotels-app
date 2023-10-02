"""Name in hotels fix

Revision ID: 87843bf432e1
Revises: f83ea80ecc73
Create Date: 2023-10-02 21:26:42.180933

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "87843bf432e1"
down_revision: Union[str, None] = "f83ea80ecc73"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("hotels", sa.Column("rooms_quantity", sa.Integer(), nullable=False))
    op.drop_column("hotels", "room_quantity")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "hotels",
        sa.Column("room_quantity", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_column("hotels", "rooms_quantity")
    # ### end Alembic commands ###
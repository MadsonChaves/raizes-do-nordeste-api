
"""adicionar restricoes nas movimentacoes de estoque

Revision ID: 5863f7e9997c
Revises: dc0a96521718
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5863f7e9997c'
down_revision: Union[str, Sequence[str], None] = 'dc0a96521718'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("movimentacoes_estoque") as batch_op:
        batch_op.create_check_constraint(
            "ck_movimentacoes_tipo_valido",
            "tipo IN ('entrada', 'saida')"
        )

        batch_op.create_check_constraint(
            "ck_movimentacoes_quantidade_positiva",
            "quantidade > 0"
        )


def downgrade() -> None:
    with op.batch_alter_table("movimentacoes_estoque") as batch_op:
        batch_op.drop_constraint(
            "ck_movimentacoes_quantidade_positiva",
            type_="check"
        )

        batch_op.drop_constraint(
            "ck_movimentacoes_tipo_valido",
            type_="check"
        )

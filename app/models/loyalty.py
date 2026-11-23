
from sqlalchemy import (
    Integer,
    DateTime,
    ForeignKey,
    String,
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from app.database.connection import Base


class LoyaltyAccount(Base):
    __tablename__ = "contas_fidelidade"

    __table_args__ = (
        CheckConstraint(
            "pontos >= 0",
            name="ck_fidelidade_pontos_nao_negativos"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        unique=True,
        nullable=False
    )

    pontos: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    criada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


class LoyaltyTransaction(Base):
    __tablename__ = "transacoes_fidelidade"

    __table_args__ = (
        CheckConstraint(
            "pontos > 0",
            name="ck_transacao_fidelidade_pontos_positivos"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    conta_id: Mapped[int] = mapped_column(
        ForeignKey("contas_fidelidade.id"),
        nullable=False
    )

    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"),
        unique=True,
        nullable=False
    )

    pontos: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    descricao: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    criada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

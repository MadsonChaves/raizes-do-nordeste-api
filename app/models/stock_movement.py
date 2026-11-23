
from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Integer,
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from app.database.connection import Base


class StockMovement(Base):
    __tablename__ = "movimentacoes_estoque"

    __table_args__ = (
        CheckConstraint(
            "tipo IN ('entrada', 'saida')",
            name="ck_movimentacoes_tipo_valido"
        ),
        CheckConstraint(
            "quantidade > 0",
            name="ck_movimentacoes_quantidade_positiva"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    estoque_id: Mapped[int] = mapped_column(
        ForeignKey("estoques.id"),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    quantidade: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    motivo: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

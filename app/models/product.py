from sqlalchemy import String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from decimal import Decimal

from app.database.connection import Base


class Product(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    unidade_id: Mapped[int] = mapped_column(
        ForeignKey("unidades.id"),
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    descricao: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    preco: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
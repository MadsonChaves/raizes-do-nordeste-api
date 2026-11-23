
from sqlalchemy import Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from app.database.connection import Base


class Stock(Base):
    __tablename__ = "estoques"

    __table_args__ = (
        CheckConstraint(
            "quantidade >= 0",
            name="ck_estoques_quantidade_nao_negativa"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id"),
        unique=True,
        nullable=False
    )

    quantidade: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

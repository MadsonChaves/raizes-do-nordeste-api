from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.dependencies import get_usuario_logado
from app.models.user import User
from app.models.loyalty import LoyaltyAccount
from app.schemas.loyalty import LoyaltyResponse


router = APIRouter(
    prefix="/fidelidade",
    tags=["Fidelidade"]
)


# Consultar saldo de pontos do cliente
@router.get("/me", response_model=LoyaltyResponse)
def consultar_fidelidade(
    db: Session = Depends(get_db),
    usuario: User = Depends(get_usuario_logado)
):
    conta = db.query(LoyaltyAccount).filter(
        LoyaltyAccount.usuario_id == usuario.id
    ).first()

    # Cria uma conta com saldo zero caso ainda não exista
    if not conta:
        conta = LoyaltyAccount(
            usuario_id=usuario.id,
            pontos=0
        )

        db.add(conta)
        db.commit()
        db.refresh(conta)

    return conta
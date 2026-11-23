
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.dependencies import exigir_perfil
from app.models.user import User
from app.models.stock_movement import StockMovement
from app.schemas.stock_movement import StockMovementResponse


router = APIRouter(
    prefix="/movimentacoes-estoque",
    tags=["Movimentações de Estoque"]
)


# Listar histórico de movimentações
@router.get("/", response_model=list[StockMovementResponse])
def listar_movimentacoes(
    db: Session = Depends(get_db),
    usuario: User = Depends(exigir_perfil("gerente", "administrador"))
):
    movimentacoes = db.query(StockMovement).order_by(
        StockMovement.id.desc()
    ).all()

    return movimentacoes

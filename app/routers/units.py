
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.dependencies import get_usuario_logado, exigir_perfil
from app.models.user import User
from app.models.unit import Unit
from app.schemas.unit import UnitCreate, UnitUpdate, UnitResponse


router = APIRouter(
    prefix="/unidades",
    tags=["Unidades"]
)


# Cadastrar uma unidade
@router.post("/", response_model=UnitResponse, status_code=status.HTTP_201_CREATED)
def criar_unidade(
    dados: UnitCreate,
    db: Session = Depends(get_db),
    usuario: User = Depends(exigir_perfil("gerente", "administrador"))
):
    unidade = Unit(**dados.model_dump())

    db.add(unidade)
    db.commit()
    db.refresh(unidade)

    return unidade


# Listar todas as unidades
@router.get("/", response_model=list[UnitResponse])
def listar_unidades(
    db: Session = Depends(get_db),
    usuario: User = Depends(get_usuario_logado)
):
    return db.query(Unit).all()


# Consultar uma unidade pelo ID
@router.get("/{unidade_id}", response_model=UnitResponse)
def buscar_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_usuario_logado)
):
    unidade = db.query(Unit).filter(Unit.id == unidade_id).first()

    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada."
        )

    return unidade


# Atualizar uma unidade
@router.patch("/{unidade_id}", response_model=UnitResponse)
def atualizar_unidade(
    unidade_id: int,
    dados: UnitUpdate,
    db: Session = Depends(get_db),
    usuario: User = Depends(exigir_perfil("gerente", "administrador"))
):
    unidade = db.query(Unit).filter(Unit.id == unidade_id).first()

    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada."
        )

    alteracoes = dados.model_dump(exclude_unset=True)

    for campo, valor in alteracoes.items():
        setattr(unidade, campo, valor)

    db.commit()
    db.refresh(unidade)

    return unidade

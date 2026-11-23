
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.dependencies import get_usuario_logado, exigir_perfil
from app.models.user import User
from app.models.product import Product
from app.models.unit import Unit
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


# Cadastrar um produto
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    dados: ProductCreate,
    db: Session = Depends(get_db),
    usuario: User = Depends(exigir_perfil("gerente", "administrador"))
):
    unidade = db.query(Unit).filter(Unit.id == dados.unidade_id).first()

    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada."
        )

    produto = Product(**dados.model_dump())

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto


# Listar todos os produtos
@router.get("/", response_model=list[ProductResponse])
def listar_produtos(
    db: Session = Depends(get_db),
    usuario: User = Depends(get_usuario_logado)
):
    return db.query(Product).all()


# Consultar um produto pelo ID
@router.get("/{produto_id}", response_model=ProductResponse)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_usuario_logado)
):
    produto = db.query(Product).filter(Product.id == produto_id).first()

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    return produto


# Atualizar um produto
@router.patch("/{produto_id}", response_model=ProductResponse)
def atualizar_produto(
    produto_id: int,
    dados: ProductUpdate,
    db: Session = Depends(get_db),
    usuario: User = Depends(exigir_perfil("gerente", "administrador"))
):
    produto = db.query(Product).filter(Product.id == produto_id).first()

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    alteracoes = dados.model_dump(exclude_unset=True)

    for campo, valor in alteracoes.items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    return produto

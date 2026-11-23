
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.dependencies import exigir_perfil
from app.models.user import User
from app.models.stock import Stock
from app.models.product import Product
from app.models.stock_movement import StockMovement
from app.schemas.stock import StockCreate, StockUpdate, StockResponse


router = APIRouter(
    prefix="/estoque",
    tags=["Estoque"]
)


# Cadastrar estoque
@router.post("/", response_model=StockResponse, status_code=201)
def cadastrar_estoque(
    dados: StockCreate,
    db: Session = Depends(get_db),
    usuario: User = Depends(exigir_perfil("gerente", "administrador"))
):
    produto = db.query(Product).filter(
        Product.id == dados.produto_id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    estoque_existente = db.query(Stock).filter(
        Stock.produto_id == dados.produto_id
    ).first()

    if estoque_existente:
        raise HTTPException(
            status_code=400,
            detail="Esse produto já possui um registro de estoque."
        )

    novo_estoque = Stock(
        produto_id=dados.produto_id,
        quantidade=dados.quantidade
    )

    db.add(novo_estoque)
    db.flush()

    # Registrar o estoque inicial no histórico
    if dados.quantidade > 0:
        movimentacao = StockMovement(
            estoque_id=novo_estoque.id,
            tipo="entrada",
            quantidade=dados.quantidade,
            motivo="Cadastro inicial do estoque"
        )

        db.add(movimentacao)

    db.commit()
    db.refresh(novo_estoque)

    return novo_estoque


# Listar estoques
@router.get("/", response_model=list[StockResponse])
def listar_estoques(
    db: Session = Depends(get_db),
    usuario: User = Depends(exigir_perfil("gerente", "administrador"))
):
    return db.query(Stock).all()


# Buscar estoque pelo ID
@router.get("/{estoque_id}", response_model=StockResponse)
def buscar_estoque(
    estoque_id: int,
    db: Session = Depends(get_db),
    usuario: User = Depends(exigir_perfil("gerente", "administrador"))
):
    estoque = db.query(Stock).filter(
        Stock.id == estoque_id
    ).first()

    if not estoque:
        raise HTTPException(
            status_code=404,
            detail="Estoque não encontrado."
        )

    return estoque


# Registrar entrada ou saída de estoque
@router.patch("/{estoque_id}", response_model=StockResponse)
def atualizar_estoque(
    estoque_id: int,
    dados: StockUpdate,
    db: Session = Depends(get_db),
    usuario: User = Depends(exigir_perfil("gerente", "administrador"))
):
    estoque = db.query(Stock).filter(
        Stock.id == estoque_id
    ).first()

    if not estoque:
        raise HTTPException(
            status_code=404,
            detail="Estoque não encontrado."
        )

    if dados.tipo == "entrada":
        estoque.quantidade += dados.quantidade

    elif dados.tipo == "saida":
        if estoque.quantidade < dados.quantidade:
            raise HTTPException(
                status_code=400,
                detail="Estoque insuficiente para realizar essa saída."
            )

        estoque.quantidade -= dados.quantidade

    movimentacao = StockMovement(
        estoque_id=estoque.id,
        tipo=dados.tipo,
        quantidade=dados.quantidade,
        motivo=dados.motivo
    )

    db.add(movimentacao)

    db.commit()
    db.refresh(estoque)

    return estoque

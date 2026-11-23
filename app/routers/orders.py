


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from app.database.dependencies import get_db
from app.core.dependencies import get_usuario_logado
from app.models.user import User
from app.models.unit import Unit
from app.models.product import Product
from app.models.stock import Stock
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderResponse
from app.models.stock_movement import StockMovement


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


# Listar pedidos do usuário logado
@router.get("/", response_model=list[OrderResponse])
def listar_pedidos(
    db: Session = Depends(get_db),
    usuario: User = Depends(get_usuario_logado)
):
    pedidos = db.query(Order).filter(
        Order.usuario_id == usuario.id
    ).all()

    resultado = []

    for pedido in pedidos:
        itens = db.query(OrderItem).filter(
            OrderItem.pedido_id == pedido.id
        ).all()

        resultado.append({
            "id": pedido.id,
            "usuario_id": pedido.usuario_id,
            "unidade_id": pedido.unidade_id,
            "canal_pedido": pedido.canal_pedido,
            "status": pedido.status,
            "valor_total": pedido.valor_total,
            "itens": itens
        })

    return resultado


# Buscar pedido específico do usuário logado
@router.get("/{pedido_id}", response_model=OrderResponse)
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_usuario_logado)
):
    pedido = db.query(Order).filter(
        Order.id == pedido_id,
        Order.usuario_id == usuario.id
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    itens = db.query(OrderItem).filter(
        OrderItem.pedido_id == pedido.id
    ).all()

    return {
        "id": pedido.id,
        "usuario_id": pedido.usuario_id,
        "unidade_id": pedido.unidade_id,
        "canal_pedido": pedido.canal_pedido,
        "status": pedido.status,
        "valor_total": pedido.valor_total,
        "itens": itens
    }


# Criar pedido
@router.post("/", response_model=OrderResponse, status_code=201)
def criar_pedido(
    dados: OrderCreate,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_usuario_logado)
):
    # Verifica se a unidade existe e está ativa
    unidade = db.query(Unit).filter(
        Unit.id == dados.unidade_id,
        Unit.ativa == True
    ).first()

    if not unidade:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada ou inativa."
        )

    # Verifica se o canal do pedido é válido
    canais_validos = [
        "aplicativo",
        "totem",
        "balcao",
        "retirada_rapida"
    ]

    if dados.canal_pedido not in canais_validos:
        raise HTTPException(
            status_code=400,
            detail="Canal de pedido inválido."
        )

    # Impede produtos repetidos no mesmo pedido
    produtos_ids = [item.produto_id for item in dados.itens]

    if len(produtos_ids) != len(set(produtos_ids)):
        raise HTTPException(
            status_code=400,
            detail="Não repita produtos no mesmo pedido."
        )

    valor_total = Decimal("0.00")
    itens_para_cadastrar = []

    # Verifica os produtos e o estoque
    for item in dados.itens:

        produto = db.query(Product).filter(
            Product.id == item.produto_id,
            Product.unidade_id == dados.unidade_id,
            Product.ativo == True
        ).first()

        if not produto:
            raise HTTPException(
                status_code=404,
                detail=f"Produto {item.produto_id} não encontrado ou inativo nesta unidade."
            )

        estoque = db.query(Stock).filter(
            Stock.produto_id == produto.id
        ).first()

        if not estoque or estoque.quantidade < item.quantidade:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente para o produto {produto.nome}."
            )

        subtotal = produto.preco * item.quantidade
        valor_total += subtotal

        itens_para_cadastrar.append({
            "produto": produto,
            "estoque": estoque,
            "quantidade": item.quantidade
        })

    # Cria o pedido
    novo_pedido = Order(
        usuario_id=usuario.id,
        unidade_id=dados.unidade_id,
        canal_pedido=dados.canal_pedido,
        status="aguardando_pagamento",
        valor_total=valor_total
    )

    db.add(novo_pedido)
    db.flush()

    # Cadastra os itens e reserva as quantidades no estoque
    for item in itens_para_cadastrar:

        novo_item = OrderItem(
            pedido_id=novo_pedido.id,
            produto_id=item["produto"].id,
            quantidade=item["quantidade"],
            preco_unitario=item["produto"].preco
        )

        item["estoque"].quantidade -= item["quantidade"]
        db.add(novo_item)

        # Registra a saída no histórico de movimentações
        movimentacao = StockMovement(
            estoque_id=item["estoque"].id,
            tipo="saida",
            quantidade=item["quantidade"],
            motivo=f"Reserva para pedido #{novo_pedido.id}"
        )

        db.add(movimentacao)

    db.commit()
    db.refresh(novo_pedido)

    # Busca os itens cadastrados para montar a resposta
    itens_resposta = db.query(OrderItem).filter(
        OrderItem.pedido_id == novo_pedido.id
    ).all()

    return {
        "id": novo_pedido.id,
        "usuario_id": novo_pedido.usuario_id,
        "unidade_id": novo_pedido.unidade_id,
        "canal_pedido": novo_pedido.canal_pedido,
        "status": novo_pedido.status,
        "valor_total": novo_pedido.valor_total,
        "itens": itens_resposta
    }

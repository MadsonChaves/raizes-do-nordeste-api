

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.dependencies import get_usuario_logado
from app.models.user import User
from app.models.order import Order, OrderItem
from app.models.stock import Stock
from app.models.payment import Payment
from app.models.stock_movement import StockMovement
from app.models.loyalty import LoyaltyAccount, LoyaltyTransaction
from app.schemas.payment import PaymentCreate, PaymentResponse


router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)


# Realizar pagamento simulado
@router.post("/", response_model=PaymentResponse, status_code=201)
def realizar_pagamento(
    dados: PaymentCreate,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_usuario_logado)
):
    # Verifica se o pedido existe e pertence ao usuário
    pedido = db.query(Order).filter(
        Order.id == dados.pedido_id,
        Order.usuario_id == usuario.id
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    # Verifica se o pedido ainda aguarda pagamento
    if pedido.status != "aguardando_pagamento":
        raise HTTPException(
            status_code=400,
            detail="Este pedido não está aguardando pagamento."
        )

    # Verifica se o pedido já possui um pagamento
    pagamento_existente = db.query(Payment).filter(
        Payment.pedido_id == pedido.id
    ).first()

    if pagamento_existente:
        raise HTTPException(
            status_code=400,
            detail="Este pedido já possui um pagamento."
        )

    # Verifica se o método de pagamento é válido
    metodos_validos = ["pix", "cartao", "dinheiro"]

    if dados.metodo not in metodos_validos:
        raise HTTPException(
            status_code=400,
            detail="Método de pagamento inválido."
        )

    # Define o resultado do pagamento simulado
    if dados.aprovado:
        status_pagamento = "aprovado"
        pedido.status = "pago"

        # Busca a conta de fidelidade do cliente
        conta = db.query(LoyaltyAccount).filter(
            LoyaltyAccount.usuario_id == usuario.id
        ).first()

        # Cria a conta caso ainda não exista
        if not conta:
            conta = LoyaltyAccount(
                usuario_id=usuario.id,
                pontos=0
            )
            db.add(conta)
            db.flush()

        # Calcula 1 ponto por real pago
        pontos = int(pedido.valor_total)

        if pontos > 0:
            conta.pontos += pontos

            # Registra a pontuação no histórico
            transacao = LoyaltyTransaction(
                conta_id=conta.id,
                pedido_id=pedido.id,
                pontos=pontos,
                descricao=f"Pontos recebidos pelo pedido #{pedido.id}"
            )

            db.add(transacao)

    else:
        status_pagamento = "recusado"
        pedido.status = "pagamento_recusado"

        # Devolve os produtos ao estoque
        itens = db.query(OrderItem).filter(
            OrderItem.pedido_id == pedido.id
        ).all()

        for item in itens:
            estoque = db.query(Stock).filter(
                Stock.produto_id == item.produto_id
            ).first()

            if estoque:
                estoque.quantidade += item.quantidade

                # Registra a devolução no histórico
                movimentacao = StockMovement(
                    estoque_id=estoque.id,
                    tipo="entrada",
                    quantidade=item.quantidade,
                    motivo=f"Devolução por pagamento recusado do pedido #{pedido.id}"
                )

                db.add(movimentacao)

    # Registra o pagamento
    novo_pagamento = Payment(
        pedido_id=pedido.id,
        valor=pedido.valor_total,
        metodo=dados.metodo,
        status=status_pagamento
    )

    db.add(novo_pagamento)
    db.commit()
    db.refresh(novo_pagamento)

    return novo_pagamento

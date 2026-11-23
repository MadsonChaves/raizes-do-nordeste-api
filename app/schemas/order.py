
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal


# Dados de cada produto dentro do pedido
class OrderItemCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)


# Dados recebidos para criar um pedido
class OrderCreate(BaseModel):
    unidade_id: int
    canal_pedido: str
    itens: list[OrderItemCreate] = Field(min_length=1)


# Dados devolvidos para cada produto do pedido
class OrderItemResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal

    model_config = ConfigDict(from_attributes=True)


# Dados devolvidos pela API
class OrderResponse(BaseModel):
    id: int
    usuario_id: int
    unidade_id: int
    canal_pedido: str
    status: str
    valor_total: Decimal
    itens: list[OrderItemResponse]


from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal


# Dados recebidos para realizar um pagamento
class PaymentCreate(BaseModel):
    pedido_id: int
    metodo: str
    aprovado: bool


# Dados devolvidos pela API
class PaymentResponse(BaseModel):
    id: int
    pedido_id: int
    valor: Decimal
    metodo: str
    status: str

    model_config = ConfigDict(from_attributes=True)



from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


# Dados recebidos para cadastrar o estoque
class StockCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(ge=0)


# Dados recebidos para movimentar o estoque
class StockUpdate(BaseModel):
    tipo: Literal["entrada", "saida"]
    quantidade: int = Field(gt=0)
    motivo: str = Field(min_length=3, max_length=200)


# Dados devolvidos pela API
class StockResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int

    model_config = ConfigDict(from_attributes=True)

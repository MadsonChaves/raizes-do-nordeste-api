from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal


# Dados recebidos ao cadastrar um produto
class ProductCreate(BaseModel):
    unidade_id: int
    nome: str
    descricao: str | None = None
    preco: Decimal = Field(gt=0)


# Dados recebidos ao atualizar um produto
class ProductUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    preco: Decimal | None = Field(default=None, gt=0)
    ativo: bool | None = None


# Dados devolvidos pela API
class ProductResponse(BaseModel):
    id: int
    unidade_id: int
    nome: str
    descricao: str | None
    preco: Decimal
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
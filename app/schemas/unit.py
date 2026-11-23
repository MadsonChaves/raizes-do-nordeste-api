from pydantic import BaseModel, ConfigDict


# Dados recebidos ao cadastrar uma unidade
class UnitCreate(BaseModel):
    nome: str
    endereco: str
    cidade: str
    estado: str


# Dados recebidos ao atualizar uma unidade
class UnitUpdate(BaseModel):
    nome: str | None = None
    endereco: str | None = None
    cidade: str | None = None
    estado: str | None = None
    ativa: bool | None = None


# Dados devolvidos pela API
class UnitResponse(BaseModel):
    id: int
    nome: str
    endereco: str
    cidade: str
    estado: str
    ativa: bool

    model_config = ConfigDict(from_attributes=True)
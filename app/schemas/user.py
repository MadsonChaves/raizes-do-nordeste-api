
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


# Dados recebidos no cadastro
class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str


# Dados devolvidos pela API
class UserResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: str
    ativo: bool
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)

# Dados recebidos no login
class UserLogin(BaseModel):
    email: EmailStr
    senha: str
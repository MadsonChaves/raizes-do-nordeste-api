from pydantic import BaseModel, ConfigDict
from datetime import datetime


class LoyaltyResponse(BaseModel):
    id: int
    usuario_id: int
    pontos: int
    criada_em: datetime

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class StockMovementResponse(BaseModel):
    id: int
    estoque_id: int
    tipo: str
    quantidade: int
    motivo: str
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)

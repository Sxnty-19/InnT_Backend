from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class Reserva(BaseModel):
    id_reserva: Optional[int] = None
    id_usuario: int
    date_start: datetime
    date_end: datetime
    tiene_ninos: Optional[bool] = False
    tiene_mascotas: Optional[bool] = False
    total_cop: Optional[Decimal]
    capacidad_total: Optional[int]
    estado: Optional[bool] = True
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReservaHabitacion(BaseModel):
    id_rxh: Optional[int] = None
    id_reserva: int
    id_habitacion: int
    estado: Optional[bool] = True
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Habitacion(BaseModel):
    id_habitacion: Optional[int] = None
    id_thabitacion: int
    numero: str
    limpieza: Optional[bool] = True
    estado: Optional[bool] = True
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None

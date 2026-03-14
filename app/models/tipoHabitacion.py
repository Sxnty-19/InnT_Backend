from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class TipoHabitacion(BaseModel):
    id_thabitacion: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    capacidad_max: int
    precio_x_dia: Decimal
    estado: Optional[bool] = True
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None

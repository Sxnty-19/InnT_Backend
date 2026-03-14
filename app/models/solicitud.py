from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Solicitud(BaseModel):
    id_solicitud: Optional[int] = None
    id_usuario: int
    id_habitacion: int
    descripcion: Optional[str] = None
    estado: Optional[bool] = True
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Modulo(BaseModel):
    id_modulo: Optional[int] = None
    nombre: str
    ruta: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[bool] = True
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None

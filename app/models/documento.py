from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Documento(BaseModel):
    id_documento: Optional[int] = None
    id_tdocumento: int
    id_usuario: int
    numero_documento: str
    lugar_expedicion: str
    url_imagen: Optional[str] = None
    documento_validado: Optional[bool] = False
    estado: Optional[bool] = True
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None

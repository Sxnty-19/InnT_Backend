from pydantic import BaseModel
from typing import List, Optional

class ReservaAux(BaseModel):
    date_start: str
    date_end: str
    tiene_ninos: Optional[bool] = False
    tiene_mascotas: Optional[bool] = False
    habitaciones: List[int]

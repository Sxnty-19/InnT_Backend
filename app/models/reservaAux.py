from pydantic import BaseModel
from typing import List, Optional

class ReservaAux(BaseModel):
    date_start: str
    date_end: str
    tiene_ninos: Optional[bool]
    tiene_mascotas: Optional[bool]
    habitaciones: List[int]

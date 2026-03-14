from pydantic import BaseModel
from typing import List

class ReservaAux(BaseModel):
    id_usuario: int
    date_start: str
    date_end: str
    habitaciones: List[int]

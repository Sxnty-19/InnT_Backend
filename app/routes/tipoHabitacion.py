from fastapi import APIRouter
from controllers.tipoHabitacion import TipoHabitacionController
from models.tipoHabitacion import TipoHabitacion

tipoHabitacion_router = APIRouter()
tipoHabitacion_controller = TipoHabitacionController()

@tipoHabitacion_router.post("/")
async def create_tipoHabitacion(tipo: TipoHabitacion):
    return tipoHabitacion_controller.create_tipoHabitacion(tipo)

@tipoHabitacion_router.get("/")
async def get_tiposHabitacion():
    return tipoHabitacion_controller.get_tiposHabitacion()

@tipoHabitacion_router.get("/{id_thabitacion}")
async def get_tipoHabitacion_id(id_thabitacion: int):
    return tipoHabitacion_controller.get_tipoHabitacion_id(id_thabitacion)

from fastapi import APIRouter, Depends
from controllers.reserva import ReservaController
from models.reserva import Reserva
from models.reservaAux import ReservaAux
from utils.auth import verificar_token

reserva_router = APIRouter()
reserva_controller = ReservaController()

@reserva_router.post("/")
async def create_reserva(reserva: Reserva):
    return reserva_controller.create_reserva(reserva)

@reserva_router.get("/")
async def get_reservas():
    return reserva_controller.get_reservas()

@reserva_router.get("/{id_reserva}")
async def get_reserva_id(id_reserva: int):
    return reserva_controller.get_reserva_id(id_reserva)

@reserva_router.get("/activas/")
async def get_reservas_activas(payload: dict = Depends(verificar_token)):
    return reserva_controller.get_reservas_activas(payload)

@reserva_router.get("/terminadas/")
async def get_reservas_terminadas(payload: dict = Depends(verificar_token)):
    return reserva_controller.get_reservas_terminadas(payload)

@reserva_router.get("/usuarios/")
async def get_reservas_usuarios():
    return reserva_controller.get_reservas_usuarios()

@reserva_router.delete("/{id_reserva}")
async def delete_reserva(id_reserva: int):
    return reserva_controller.delete_reserva(id_reserva)

@reserva_router.post("/habitaciones/")
async def create_reserva_habitaciones(data: ReservaAux, payload: dict = Depends(verificar_token), ):
    return reserva_controller.create_reserva_habitaciones(
        payload["id_usuario"],
        data.date_start,
        data.date_end,
        data.tiene_ninos,
        data.tiene_mascotas,
        data.habitaciones
    )

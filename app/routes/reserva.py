from fastapi import APIRouter
from controllers.reserva import ReservaController
from models.reserva import Reserva
from models.reservaAux import ReservaAux

reserva_router = APIRouter()
reserva_controller = ReservaController()

@reserva_router.post("/create_reserva") #
async def create_reserva(reserva: Reserva):
    rpta = reserva_controller.create_reserva(reserva)
    return rpta

@reserva_router.get("/get_reservas") #
async def get_reservas():
    rpta = reserva_controller.get_reservas()
    return rpta

@reserva_router.get("/get_reserva/{id_reserva}") #
async def get_reserva_id(id_reserva: int):
    rpta = reserva_controller.get_reserva_id(id_reserva)
    return rpta

@reserva_router.get("/activas/{id_usuario}") #
async def get_reservas_activas(id_usuario: int):
    rpta = reserva_controller.get_reservas_activas(id_usuario)
    return rpta

@reserva_router.get("/terminadas/{id_usuario}") #
async def get_reservas_terminadas(id_usuario: int):
    rpta = reserva_controller.get_reservas_terminadas(id_usuario)
    return rpta

@reserva_router.get("/usuarios/")
async def get_reservas_usuarios(id_reserva: int):
    rpta = reserva_controller.get_reservas_usuarios(id_reserva)
    return rpta

@reserva_router.delete("/cancelar/{id_reserva}")
async def delete_reserva(id_reserva: int):
    rpta = reserva_controller.delete_reserva(id_reserva)
    return rpta

@reserva_router.post("/create_with_rooms") #
async def create_reserva_habitaciones(payload: ReservaAux):
    rpta = reserva_controller.create_reserva_habitaciones(
        payload.id_usuario,
        payload.date_start,
        payload.date_end,
        payload.habitaciones
    )
    return rpta

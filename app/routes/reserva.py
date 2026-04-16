from fastapi import APIRouter, Depends
from controllers.reserva import ReservaController
from models.reserva import Reserva
from models.reservaAux import ReservaAux
from utils.auth import verificar_token

reserva_router = APIRouter()
reserva_controller = ReservaController()

# Crear reserva
@reserva_router.post("/")
async def create_reserva(reserva: Reserva):
    return reserva_controller.create_reserva(reserva)

# Obtener todas las reservas
@reserva_router.get("/")
async def get_reservas():
    return reserva_controller.get_reservas()

# Obtener reserva por id
@reserva_router.get("/{id_reserva}")
async def get_reserva_id(id_reserva: int):
    return reserva_controller.get_reserva_id(id_reserva)

# Obtener reservas activas
@reserva_router.get("/activas/")
async def get_reservas_activas(payload: dict = Depends(verificar_token)):
    return reserva_controller.get_reservas_activas(payload)

# Obtener reservas terminadas
@reserva_router.get("/terminadas/")
async def get_reservas_terminadas(payload: dict = Depends(verificar_token)):
    return reserva_controller.get_reservas_terminadas(payload)

# Obtener reservas por usuario
@reserva_router.get("/usuarios/")
async def get_reservas_usuarios():
    return reserva_controller.get_reservas_usuarios()

# Eliminar reserva
@reserva_router.delete("/{id_reserva}")
async def delete_reserva(id_reserva: int):
    return reserva_controller.delete_reserva(id_reserva)

# Crear reserva con habitaciones
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

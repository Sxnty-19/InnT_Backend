from fastapi import APIRouter
from controllers.reservaHabitacion import ReservaHabitacionController
from models.reservaHabitacion import ReservaHabitacion

reservaHabitacion_router = APIRouter()
reservaHabitacion_controller = ReservaHabitacionController()

@reservaHabitacion_router.post("/")
async def create_reservaHabitacion(reserva_habitacion: ReservaHabitacion):
    return reservaHabitacion_controller.create_reservaHabitacion(reserva_habitacion)

@reservaHabitacion_router.get("/")
async def get_reservaHabitaciones():
    return reservaHabitacion_controller.get_reservaHabitaciones()

@reservaHabitacion_router.get("/{id_rxh}")
async def get_reservaHabitacion_id(id_rxh: int):
    return reservaHabitacion_controller.get_reservaHabitacion_id(id_rxh)

from fastapi import APIRouter
from controllers.reservaHabitacion import ReservaHabitacionController
from models.reservaHabitacion import ReservaHabitacion

reservaHabitacion_router = APIRouter()
reservaHabitacion_controller = ReservaHabitacionController()

@reservaHabitacion_router.post("/create_reserva_habitacion")
async def create_reservaHabitacion(reserva_habitacion: ReservaHabitacion):
    rpta = reservaHabitacion_controller.create_reservaHabitacion(reserva_habitacion)
    return rpta

@reservaHabitacion_router.get("/get_reservas_habitaciones")
async def get_reservaHabitaciones():
    rpta = reservaHabitacion_controller.get_reservaHabitaciones()
    return rpta

@reservaHabitacion_router.get("/get_reserva_habitacion/{id_rxh}")
async def get_reservaHabitacion_id(id_rxh: int):
    rpta = reservaHabitacion_controller.get_reservaHabitacion_id(id_rxh)
    return rpta

from fastapi import APIRouter, Depends
from controllers.habitacion import HabitacionController
from models.habitacion import Habitacion

habitacion_router = APIRouter()
habitacion_controller = HabitacionController()

@habitacion_router.post("/")
def create_habitacion(habitacion: Habitacion):
    return habitacion_controller.create_habitacion(habitacion)

@habitacion_router.get("/")
def get_habitaciones():
    return habitacion_controller.get_habitaciones()

@habitacion_router.get("/{id_habitacion}")
def get_habitacion_id(id_habitacion: int):
    return habitacion_controller.get_habitacion_id(id_habitacion)

@habitacion_router.get("/disponibles/")
def get_disponibles(date_start: str, date_end: str):
    return habitacion_controller.get_disponibles(date_start, date_end)

@habitacion_router.put("/{id_habitacion}")
def update_limpieza(id_habitacion: int):
    return habitacion_controller.update_limpieza(id_habitacion)

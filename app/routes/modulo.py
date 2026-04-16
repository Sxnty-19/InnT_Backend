from fastapi import APIRouter
from controllers.modulo import ModuloController
from models.modulo import Modulo

modulo_router = APIRouter()
modulo_controller = ModuloController()

@modulo_router.post("/")
async def create_modulo(modulo: Modulo):
    return modulo_controller.create_modulo(modulo)

@modulo_router.get("/")
async def get_modulos():
    return modulo_controller.get_modulos()

@modulo_router.get("/{id_modulo}")
async def get_modulo_id(id_modulo: int):
    return modulo_controller.get_modulo_id(id_modulo)

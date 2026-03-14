from fastapi import APIRouter
from controllers.modulo import ModuloController
from models.modulo import Modulo

modulo_router = APIRouter()
modulo_controller = ModuloController()

# Crear un nuevo módulo
@modulo_router.post("/")
async def create_modulo(modulo: Modulo):
    return modulo_controller.create_modulo(modulo)

# Obtener todos los módulos
@modulo_router.get("/")
async def get_modulos():
    return modulo_controller.get_modulos()

# Obtener un módulo por id
@modulo_router.get("/{id_modulo}")
async def get_modulo_id(id_modulo: int):
    return modulo_controller.get_modulo_id(id_modulo)

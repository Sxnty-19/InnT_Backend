from fastapi import APIRouter
from controllers.rol import RolController
from models.rol import Rol

rol_router = APIRouter()
rol_controller = RolController()

@rol_router.post("/")
async def create_rol(rol: Rol):
    rpta = rol_controller.create_rol(rol)
    return rpta

@rol_router.get("/")
async def get_roles():
    rpta = rol_controller.get_roles()
    return rpta

@rol_router.get("/{id_rol}")
async def get_rol_id(id_rol: int):
    rpta = rol_controller.get_rol_id(id_rol)
    return rpta

@rol_router.get("/roles/")
async def get_roles_activos():
    rpta = rol_controller.get_roles_activos()
    return rpta

@rol_router.put("/{id_rol}")
async def update_rol(id_rol: int):
    rpta = rol_controller.update_rol(id_rol)
    return rpta
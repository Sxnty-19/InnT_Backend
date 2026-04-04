from fastapi import APIRouter
from controllers.rol import RolController
from models.rol import Rol

rol_router = APIRouter()
rol_controller = RolController()

@rol_router.post("/")
async def create_rol(rol: Rol):
    return rol_controller.create_rol(rol)

@rol_router.get("/")
async def get_roles():
    return rol_controller.get_roles()

@rol_router.get("/{id_rol}")
async def get_rol_id(id_rol: int):
    return rol_controller.get_rol_id(id_rol)

@rol_router.get("/roles/")
async def get_roles_activos():
    return rol_controller.get_roles_activos()

@rol_router.put("/{id_rol}")
async def update_estado(id_rol: int):
    return rol_controller.update_estado(id_rol)

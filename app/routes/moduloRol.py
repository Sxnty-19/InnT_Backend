from fastapi import APIRouter, Depends
from controllers.moduloRol import ModuloRolController
from models.moduloRol import ModuloRol
from utils.auth import verificar_token

moduloRol_router = APIRouter()
moduloRol_controller = ModuloRolController()

@moduloRol_router.post("/")
def create_moduloRol(modulo_rol: ModuloRol):
    return moduloRol_controller.create_moduloRol(modulo_rol)

@moduloRol_router.get("/")
def get_modulosRol():
    return moduloRol_controller.get_modulosRol()

@moduloRol_router.get("/{id_mxr}")
def get_moduloRol_id(id_mxr: int):
    return moduloRol_controller.get_moduloRol_id(id_mxr)

@moduloRol_router.get("/rol/")
def get_modulos_rol(payload: dict = Depends(verificar_token)):
    return moduloRol_controller.get_modulos_rol(payload)

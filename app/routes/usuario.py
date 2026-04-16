from fastapi import APIRouter, Depends
from controllers.usuario import UsuarioController
from models.usuario import Usuario
from utils.auth import verificar_token

usuario_router = APIRouter()
usuario_controller = UsuarioController()

@usuario_router.post("/")
async def create_usuario(usuario: Usuario):
    return usuario_controller.create_usuario(usuario)

@usuario_router.get("/")
async def get_usuarios():
    return usuario_controller.get_usuarios()

@usuario_router.get("/id/")
async def get_usuario_id(payload: dict = Depends(verificar_token)):
    return usuario_controller.get_usuario_id(payload)

@usuario_router.patch("/")
async def update_usuario(usuario: Usuario, payload: dict = Depends(verificar_token)):
    data = usuario.dict(exclude_unset=True)
    return usuario_controller.update_usuario(data, payload)

@usuario_router.put("/rol/{id_usuario}/{id_rol}")
async def update_rol(id_usuario: int, id_rol: int):
    return usuario_controller.update_rol(id_usuario, id_rol)

@usuario_router.put("/estado/{id_usuario}")
async def update_estado(id_usuario: int):
    return usuario_controller.update_estado(id_usuario)

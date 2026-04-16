from fastapi import APIRouter, Form
from controllers.auth import AuthController
from models.usuario import Usuario

auth_router = APIRouter()
auth_controller = AuthController()

@auth_router.post("/register")
async def register_user(usuario: Usuario):
    return auth_controller.register_user(usuario)

@auth_router.post("/login")
async def login_user(username: str = Form(...), password: str = Form(...)):
    return auth_controller.login_user(username, password)

@auth_router.post("/login-azure")
async def login_azure(correo: str = Form(...)):
    return auth_controller.login_azure(correo)

from fastapi import APIRouter
from controllers.usuarioHabitacion import UsuarioHabitacionController
from models.usuarioHabitacion import UsuarioHabitacion

usuarioHabitacion_router = APIRouter()
usuarioHabitacion_controller = UsuarioHabitacionController()

# Crear una relación usuario-habitación
@usuarioHabitacion_router.post("/")
async def create_usuarioHabitacion(usuario_habitacion: UsuarioHabitacion):
    return usuarioHabitacion_controller.create_usuarioHabitacion(usuario_habitacion)

# Obtener todas las relaciones usuario-habitación
@usuarioHabitacion_router.get("/")
async def get_usuariosHabitacion():
    return usuarioHabitacion_controller.get_usuariosHabitacion()

# Obtener una relación usuario-habitación por ID
@usuarioHabitacion_router.get("/{id_uxh}")
async def get_usuarioHabitacion_id(id_uxh: int):
    return usuarioHabitacion_controller.get_usuarioHabitacion_id(id_uxh)

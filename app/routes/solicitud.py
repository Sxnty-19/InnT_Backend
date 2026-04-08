from fastapi import APIRouter, Depends,Form
from controllers.solicitud import SolicitudController
from models.solicitud import Solicitud
from utils.auth import verificar_token

solicitud_router = APIRouter()
solicitud_controller = SolicitudController()

@solicitud_router.post("/")
async def create_solicitud(solicitud: Solicitud):
    return solicitud_controller.create_solicitud(solicitud)

@solicitud_router.get("/")
async def get_solicitudes():
    return solicitud_controller.get_solicitudes()

@solicitud_router.get("/{id_solicitud}")
async def get_solicitud_id(id_solicitud: int):
    return solicitud_controller.get_solicitud_id(id_solicitud)

@solicitud_router.get("/usuario/")
async def get_solicitudes_usuario(payload: dict = Depends(verificar_token)):
    return solicitud_controller.get_solicitudes_usuario(payload)

@solicitud_router.post("/habitacion/")
async def create_solicitud_habitacion(payload: dict = Depends(verificar_token), numero_habitacion: str = Form(...), descripcion: str = Form(...), estado: bool = Form(True)):
    return solicitud_controller.create_solicitud_habitacion(payload, numero_habitacion, descripcion, estado)

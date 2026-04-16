from fastapi import APIRouter
from controllers.tipoDocumento import TipoDocumentoController
from models.tipoDocumento import TipoDocumento

tipoDocumento_router = APIRouter()
tipoDocumento_controller = TipoDocumentoController()

@tipoDocumento_router.post("/")
async def create_tipoDocumento(tipo: TipoDocumento):
    return tipoDocumento_controller.create_tipoDocumento(tipo)

@tipoDocumento_router.get("/")
async def get_tiposDocumento():
    return tipoDocumento_controller.get_tiposDocumento()

@tipoDocumento_router.get("/{id_tdocumento}")
async def get_tipoDocumento_id(id_tdocumento: int):
    return tipoDocumento_controller.get_tipoDocumento_id(id_tdocumento)

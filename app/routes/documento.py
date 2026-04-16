from fastapi import APIRouter, Depends
from controllers.documento import DocumentoController
from models.documento import Documento
from utils.auth import verificar_token

documento_router = APIRouter()
documento_controller = DocumentoController()

@documento_router.post("/")
def create_documento(documento: Documento):
    return documento_controller.create_documento(documento)

@documento_router.get("/")
def get_documentos():
    return documento_controller.get_documentos()

@documento_router.get("/{id_documento}")
def get_documento_id(id_documento: int):
    return documento_controller.get_documento_id(id_documento)

@documento_router.get("/usuarios/")
def get_documentos_usuarios():
    return documento_controller.get_documentos_usuarios()

@documento_router.get("/usuario/")
def get_documentos_usuario(payload: dict = Depends(verificar_token)):
    return documento_controller.get_documentos_usuario(payload)

@documento_router.delete("/{id_documento}")
def delete_documento(id_documento: int):
    return documento_controller.delete_documento(id_documento)

@documento_router.get("/buscar/{numero_documento}")
def get_usuario_documento(numero_documento: str):
    return documento_controller.get_usuario_documento(numero_documento)

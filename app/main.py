from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import auth_router
from routes.documento import documento_router
from routes.habitacion import habitacion_router
from routes.modulo import modulo_router
from routes.moduloRol import moduloRol_router
from routes.reserva import reserva_router
from routes.reservaHabitacion import reservaHabitacion_router
from routes.rol import rol_router
from routes.solicitud import solicitud_router
from routes.tipoDocumento import tipoDocumento_router
from routes.tipoHabitacion import tipoHabitacion_router

from utils.auth import verificar_token

app = FastAPI(
    title="InnT_Backend",
    description="Backend desarrollado con FastAPI.",
    version="2.4.6"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/", methods=["GET", "HEAD"], tags=["Sistema"])
async def root():
    return {"message": "InnT_Backend en funcionamiento..."}

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(documento_router, prefix="/documentos", tags=["Documentos"], dependencies=[Depends(verificar_token)])
app.include_router(habitacion_router, prefix="/habitaciones", tags=["Habitaciones"], dependencies=[Depends(verificar_token)])
app.include_router(modulo_router, prefix="/modulos", tags=["Modulos"], dependencies=[Depends(verificar_token)])
app.include_router(moduloRol_router, prefix="/modulos-roles", tags=["Módulos-Roles"], dependencies=[Depends(verificar_token)])
app.include_router(reserva_router, prefix="/reservas", tags=["Reservas"], dependencies=[Depends(verificar_token)])
app.include_router(reservaHabitacion_router, prefix="/reservas-habitaciones", tags=["Reservas-Habitaciones"], dependencies=[Depends(verificar_token)])
app.include_router(rol_router, prefix="/roles", tags=["Roles"], dependencies=[Depends(verificar_token)])
app.include_router(solicitud_router, prefix="/solicitudes", tags=["Solicitudes"], dependencies=[Depends(verificar_token)])
app.include_router(tipoDocumento_router, prefix="/tipos-documento", tags=["Tipos de Documento"], dependencies=[Depends(verificar_token)])
app.include_router(tipoHabitacion_router, prefix="/tipos-habitacion", tags=["Tipos de Habitación"],dependencies=[Depends(verificar_token)])

#uvicorn main:app --reload
#fastapi dev main.py

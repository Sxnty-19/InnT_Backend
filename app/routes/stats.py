from fastapi import APIRouter, Depends
from controllers.stats import StatsController
from utils.auth import verificar_token

stats_router = APIRouter()
stats_controller = StatsController()

    # Indicadores

@stats_router.get("/total-usuarios")
async def get_total_usuarios(payload: dict = Depends(verificar_token)):
    return stats_controller.get_total_usuarios()

@stats_router.get("/reservas-programadas")
async def get_reservas_programadas(payload: dict = Depends(verificar_token)):
    return stats_controller.get_reservas_programadas()

@stats_router.get("/habitaciones-disponibles")
async def get_habitaciones_disponibles(payload: dict = Depends(verificar_token)):
    return stats_controller.get_habitaciones_disponibles()

@stats_router.get("/ingresos-mes")
async def get_ingresos_mes(payload: dict = Depends(verificar_token)):
    return stats_controller.get_ingresos_mes()

    # Graficas

@stats_router.get("/reservas-mes")
async def get_reservas_por_mes(payload: dict = Depends(verificar_token)):
    return stats_controller.get_reservas_por_mes()

@stats_router.get("/ingresos-mes-chart")
async def get_ingresos_por_mes(payload: dict = Depends(verificar_token)):
    return stats_controller.get_ingresos_por_mes()

@stats_router.get("/tipos-habitacion")
async def get_tipos_habitacion(payload: dict = Depends(verificar_token)):
    return stats_controller.get_tipos_habitacion()

@stats_router.get("/usuarios-rol")
async def get_usuarios_por_rol(payload: dict = Depends(verificar_token)):
    return stats_controller.get_usuarios_por_rol()

@stats_router.get("/habitaciones-tipo")
async def get_habitaciones_por_tipo(payload: dict = Depends(verificar_token)):
    return stats_controller.get_habitaciones_por_tipo()

@stats_router.get("/solicitudes-dia")
async def get_solicitudes_por_dia(payload: dict = Depends(verificar_token)):
    return stats_controller.get_solicitudes_por_dia()

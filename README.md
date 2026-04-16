# InnTech - Plataforma Hotelera (Backend)

Backend desarrollado con FastAPI para la plataforma hotelera InnTech.

## 🔧 Descripción

Este proyecto ofrece una API REST para la gestión de:
- Autenticación de usuarios
- Documentos asociados a usuarios
- Habitaciones y disponibilidad
- Reservas y reservas de habitaciones
- Solicitudes internas de habitación
- Roles, módulos y permisos
- Tipos de documentos y tipos de habitaciones
- Relaciones entre usuarios y habitaciones

## 🚀 Tecnologías

- Python
- FastAPI
- Uvicorn

## 📦 Instalación

1. Clonar el repositorio.
2. Crear y activar el entorno virtual.
3. Instalar dependencias:

```bash
cd InnT_Backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
```

## ▶️ Ejecución

Iniciar el servidor con Uvicorn desde la carpeta `app`:

```bash
cd app
uvicorn main:app --reload
```

El backend quedará disponible en `http://127.0.0.1:8000`.

## 📚 Rutas disponibles

### Sistema
- `GET /` - Estado del backend

### Auth
- `POST /auth/register` - Registrar nuevo usuario
- `POST /auth/login` - Iniciar sesión con usuario y contraseña
- `POST /auth/login-azure` - Iniciar sesión con correo (Azure)

> Las demás rutas requieren token y verifican sesión.

### Documentos
- `POST /documentos/` - Crear documento
- `GET /documentos/` - Obtener todos los documentos
- `GET /documentos/{id_documento}` - Obtener documento por ID
- `GET /documentos/usuarios/` - Obtener documentos con datos de usuario
- `GET /documentos/usuario/` - Obtener documentos del usuario autenticado
- `DELETE /documentos/{id_documento}` - Eliminar documento
- `GET /documentos/buscar/{numero_documento}` - Buscar documento por número

### Habitaciones
- `POST /habitaciones/` - Crear habitación
- `GET /habitaciones/` - Listar habitaciones
- `GET /habitaciones/{id_habitacion}` - Obtener habitación por ID
- `GET /habitaciones/disponibles/` - Consultar habitaciones disponibles por rango de fechas
- `PUT /habitaciones/{id_habitacion}` - Actualizar estado de limpieza

### Módulos
- `POST /modulos/` - Crear módulo
- `GET /modulos/` - Listar módulos
- `GET /modulos/{id_modulo}` - Obtener módulo por ID

### Módulos-Roles
- `POST /modulos-roles/` - Crear relación módulo-rol
- `GET /modulos-roles/` - Listar relaciones módulo-rol
- `GET /modulos-roles/{id_mxr}` - Obtener relación por ID
- `GET /modulos-roles/rol/` - Obtener módulos del rol del usuario autenticado

### Reservas
- `POST /reservas/` - Crear reserva
- `GET /reservas/` - Listar reservas
- `GET /reservas/{id_reserva}` - Obtener reserva por ID
- `GET /reservas/activas/` - Reservas activas del usuario autenticado
- `GET /reservas/terminadas/` - Reservas terminadas del usuario autenticado
- `GET /reservas/usuarios/` - Reservas con datos de usuario
- `DELETE /reservas/{id_reserva}` - Eliminar reserva
- `POST /reservas/habitaciones/` - Crear reserva con habitaciones

### Reservas-Habitaciones
- `POST /reservas-habitaciones/` - Crear reserva-habitación
- `GET /reservas-habitaciones/` - Listar reservas-habitaciones
- `GET /reservas-habitaciones/{id_rxh}` - Obtener reserva-habitación por ID

### Roles
- `POST /roles/` - Crear rol
- `GET /roles/` - Listar roles
- `GET /roles/{id_rol}` - Obtener rol por ID
- `GET /roles/roles/` - Listar roles activos
- `PUT /roles/{id_rol}` - Actualizar estado de rol

### Solicitudes
- `POST /solicitudes/` - Crear solicitud
- `GET /solicitudes/` - Listar solicitudes
- `GET /solicitudes/{id_solicitud}` - Obtener solicitud por ID
- `GET /solicitudes/usuario/` - Solicitudes del usuario autenticado
- `POST /solicitudes/habitacion/` - Crear solicitud de habitación
- `PUT /solicitudes/{id_solicitud}` - Actualizar estado de solicitud

### Tipos de Documento
- `POST /tipos-documento/` - Crear tipo de documento
- `GET /tipos-documento/` - Listar tipos de documento
- `GET /tipos-documento/{id_tdocumento}` - Obtener tipo de documento por ID

### Tipos de Habitación
- `POST /tipos-habitacion/` - Crear tipo de habitación
- `GET /tipos-habitacion/` - Listar tipos de habitación
- `GET /tipos-habitacion/{id_thabitacion}` - Obtener tipo de habitación por ID

### Usuarios
- `POST /usuarios/` - Crear usuario
- `GET /usuarios/` - Listar usuarios
- `GET /usuarios/id/` - Obtener usuario autenticado
- `PATCH /usuarios/` - Actualizar usuario autenticado
- `PUT /usuarios/rol/{id_usuario}/{id_rol}` - Asignar rol a usuario
- `PUT /usuarios/estado/{id_usuario}` - Cambiar estado de usuario

### Usuarios-Habitaciones
- `POST /usuarios_habitaciones/` - Crear relación usuario-habitación
- `GET /usuarios_habitaciones/` - Listar relaciones usuario-habitación
- `GET /usuarios_habitaciones/{id_uxh}` - Obtener relación por ID

## 📌 Notas

- Las rutas protegidas usan `verificar_token` para validar el token JWT.
- La configuración CORS permite acceso desde `http://localhost:4200` y `https://inn-t-frontend.vercel.app`.
- La API está pensada para integrarse con un frontend de gestión hotelera.

## 💡 Recomendaciones

- Usar `http://127.0.0.1:8000/docs` para explorar los endpoints con Swagger.
- Configurar variables de entorno y la base de datos según los controladores y modelos.

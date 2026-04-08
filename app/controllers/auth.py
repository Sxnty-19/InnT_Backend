import psycopg2
from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from config.neonConfig import connection_neon
from models.usuario import Usuario
from utils.auth import crear_token
from utils.password import encriptar_password , verificar_password
from utils.time import get_date

class AuthController:

    def register_user(self, usuario: Usuario):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            id_rol = 3
            date = get_date()

            if usuario.telefono:
                cursor.execute(
                    "SELECT 1 FROM usuario WHERE telefono = %s", (usuario.telefono,)
                )
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="El teléfono ya está en uso")

            if usuario.correo:
                cursor.execute(
                    "SELECT 1 FROM usuario WHERE correo = %s", (usuario.correo,)
                )
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="El correo ya está en uso")

            if usuario.username:
                cursor.execute(
                    "SELECT 1 FROM usuario WHERE username = %s", (usuario.username,)
                )
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="El username ya está en uso")

            password = encriptar_password(usuario.password)

            query = """
                INSERT INTO usuario (
                    id_rol,
                    primer_nombre,
                    segundo_nombre,
                    primer_apellido,
                    segundo_apellido,
                    telefono,
                    correo,
                    username,
                    password,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_usuario
            """
            values = (
                id_rol,
                usuario.primer_nombre,
                usuario.segundo_nombre,
                usuario.primer_apellido,
                usuario.segundo_apellido,
                usuario.telefono,
                usuario.correo,
                usuario.username,
                password,
                usuario.estado,
                date,
                date
            )
            cursor.execute(query, values)
            new_id = cursor.fetchone()["id_usuario"]
            conn.commit()

            return {
                "success": True,
                "message": "Usuario registrado exitosamente",
                "id_usuario": new_id
            }
        
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(err)}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def login_user(self, username: str, password: str):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    u.id_usuario,
                    u.password,
                    u.primer_nombre,
                    u.segundo_nombre,
                    u.primer_apellido,
                    u.segundo_apellido,
                    r.id_rol,
                    r.nombre
                FROM usuario u
                INNER JOIN rol r ON u.id_rol = r.id_rol
                WHERE u.username = %s AND u.estado = true
            """, (username,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Usuario o Contraseña Incorrectos")

            id_usuario = data["id_usuario"]
            password_db = data["password"]
            primer_nombre = data["primer_nombre"]
            segundo_nombre = data["segundo_nombre"] or ""
            primer_apellido = data["primer_apellido"]
            segundo_apellido = data["segundo_apellido"]

            id_rol = data["id_rol"]
            nombre_rol = data["nombre"]

            if not verificar_password(password, password_db):
                raise HTTPException(status_code=404, detail="Usuario o Contraseña Incorrectos")

            nombre_completo = f"{primer_nombre} {segundo_nombre} {primer_apellido} {segundo_apellido}".strip()

            payload = {
                "id_usuario": id_usuario,
                "id_rol": id_rol
            }

            token = crear_token(payload)

            return {
                "success": True,
                "access_token": token,
                "token_type": "bearer",
                "user": {
                    "nombre": nombre_completo,
                    "id_usuario": id_usuario,   
                    "rol": nombre_rol,
                    "id_rol": id_rol
                }
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"ERROR en la base de datos: {str(err)}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
  
    def login_azure(self, correo: str):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    u.id_usuario,
                    u.primer_nombre,
                    u.segundo_nombre,
                    u.primer_apellido,
                    u.segundo_apellido,
                    r.id_rol,
                    r.nombre
                FROM usuario u
                INNER JOIN rol r ON u.id_rol = r.id_rol
                WHERE u.correo = %s AND u.estado = true
            """, (correo,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Usuario no registrado")

            id_usuario = data["id_usuario"]
            primer_nombre = data["primer_nombre"]
            segundo_nombre = data["segundo_nombre"] or ""
            primer_apellido = data["primer_apellido"]
            segundo_apellido = data["segundo_apellido"]

            id_rol = data["id_rol"]
            nombre_rol = data["nombre"]

            nombre_completo = f"{primer_nombre} {segundo_nombre} {primer_apellido} {segundo_apellido}".strip()

            payload = {
                "id_usuario": id_usuario,
                "id_rol": id_rol
            }

            token = crear_token(payload)

            return {
                "success": True,
                "access_token": token,
                "token_type": "bearer",
                "user": {
                    "nombre": nombre_completo,
                    "id_usuario": id_usuario,
                    "rol": nombre_rol,
                    "id_rol": id_rol
                }
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"ERROR en la base de datos: {str(err)}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

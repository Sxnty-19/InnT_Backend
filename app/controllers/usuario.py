import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor
from config.neonConfig import connection_neon
from utils.password import encriptar_password
from utils.time import get_date
from models.usuario import Usuario

class UsuarioController:

    def create_usuario(self, usuario: Usuario):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()
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
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_usuario
            """
            values = (
                usuario.id_rol,
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
                "message": "Usuario creado correctamente.",
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

    def get_usuarios(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    u.*, 
                    r.nombre AS nombre_rol
                FROM usuario u
                JOIN rol r ON u.id_rol = r.id_rol
            """)

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay usuarios registrados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
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

    def get_usuario_id(self, payload: dict):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            id_usuario = payload["id_usuario"]


            cursor.execute("""
                SELECT *
                FROM usuario
                WHERE id_usuario = %s
            """, (id_usuario,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Usuario no encontrado.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
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

    def update_usuario(self, data: dict, payload: dict):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            id_usuario = payload["id_usuario"]

            campos_permitidos = {
                "primer_nombre",
                "segundo_nombre",
                "primer_apellido",
                "segundo_apellido",
                "telefono"
            }

            cursor.execute("""
                SELECT 1 FROM usuario
                WHERE id_usuario = %s
            """,(id_usuario,))

            aux = cursor.fetchone()

            if not aux:
                raise HTTPException(status_code=404, detail="Usuario no encontrado.")

            data = {k: v for k, v in data.items() if k in campos_permitidos}

            if not data:
                raise HTTPException(status_code=400, detail="No hay campos válidos para actualizar")

            campos = ", ".join([f"{key} = %s" for key in data.keys()])
            values = list(data.values())

            query = f"""
                UPDATE usuario 
                SET {campos}, date_updated = %s
                WHERE id_usuario = %s
            """

            values.append(get_date())
            values.append(id_usuario)

            cursor.execute(query, values)
            conn.commit()

            return {
                "success": True,
                "message": "Usuario actualizado correctamente"
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

    def update_rol(self, id_usuario: int, id_rol: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            cursor.execute("""
                SELECT 1 FROM usuario
                WHERE id_usuario = %s
            """,(id_usuario,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Usuario no encontrado.")

            cursor.execute("""
                UPDATE usuario
                SET id_rol = %s,
                    date_updated = %s
                WHERE id_usuario = %s
            """, (id_rol, date, id_usuario))
            conn.commit()

            return {
                "success": True,
                "message": f"Rol del usuario con id {id_usuario} actualizado correctamente."
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

    def update_estado(self, id_usuario: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            cursor.execute("""
                SELECT estado FROM usuario
                WHERE id_usuario = %s
            """,(id_usuario,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Usuario no encontrado.")

            new_estado = not data["estado"]

            cursor.execute("""
                UPDATE usuario
                SET estado = %s,
                    date_updated = %s
                WHERE id_usuario = %s
            """, (new_estado, date, id_usuario))
            conn.commit()

            return {
                "success": True,
                "message": "Estado de usuario actualizado."
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

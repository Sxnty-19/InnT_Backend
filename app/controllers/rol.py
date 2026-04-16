import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor
from config.neonConfig import connection_neon
from models.rol import Rol
from utils.time import get_date

class RolController:

    def create_rol(self, rol: Rol):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            query = """
                INSERT INTO rol (
                    nombre,
                    descripcion,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s)
                RETURNING id_rol
            """
            values = (
                rol.nombre,
                rol.descripcion,
                rol.estado,
                date,
                date
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()["id_rol"]
            conn.commit()

            return {
                "success": True,
                "message": "Rol creado correctamente.",
                "id_rol": new_id
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

    def get_roles(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("SELECT * FROM rol")

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay roles registrados.")

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

    def get_rol_id(self, id_rol: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT * FROM rol
                WHERE id_rol = %s
            """, (id_rol,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Rol no encontrado.")

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

    def get_roles_activos(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    id_rol, 
                    nombre,
                    estado
                FROM rol 
                WHERE estado = TRUE
                ORDER BY nombre
            """)

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay roles registrados.")

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

    def update_estado(self, id_rol:int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            fecha_actual = get_date()

            cursor.execute("""
                SELECT estado FROM rol
                WHERE id_rol = %s
            """,(id_rol,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Rol no encontrado.")

            new_estado = not data["estado"]

            cursor.execute("""
                UPDATE rol
                SET estado = %s,
                    date_updated = %s
                WHERE id_rol = %s
            """, (new_estado, fecha_actual, id_rol))
            conn.commit()

            return {
                "success": True,
                "message": "Estado de rol actualizado."
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

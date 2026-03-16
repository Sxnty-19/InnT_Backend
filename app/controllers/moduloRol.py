import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor
from config.neonConfig import connection_neon
from models.moduloRol import ModuloRol
from utils.time import get_date

class ModuloRolController:

    def create_moduloRol(self, modulo_rol: ModuloRol):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            query = """
                INSERT INTO modulo_rol (
                    id_modulo,
                    id_rol,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_mxr;
            """
            values = (
                modulo_rol.id_modulo,
                modulo_rol.id_rol,
                modulo_rol.estado,
                date,
                date
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()["id_mxr"]
            conn.commit()

            return {
                "success": True,
                "message": "Relación módulo-rol creada correctamente.",
                "id_mxr": new_id
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

    def get_modulosRol(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("SELECT * FROM modulo_rol")

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay relaciones registradas.")

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

    def get_moduloRol_id(self, id_mxr: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM modulo_rol
                WHERE id_mxr = %s
            """, (id_mxr,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Relación no encontrada.")

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

    def get_modulos_rol(self, payload: dict):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            id_rol = payload.get("id_rol")

            cursor.execute("""
                SELECT 
                    m.id_modulo,
                    m.nombre,
                    m.ruta
                FROM modulo_rol mr
                INNER JOIN modulo m 
                    ON mr.id_modulo = m.id_modulo
                WHERE mr.id_rol = %s
                AND mr.estado = TRUE
                AND m.estado = TRUE
            """, (id_rol,))

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="Este rol no tiene módulos asignados.")

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

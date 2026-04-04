import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor
from config.neonConfig import connection_neon
from models.solicitud import Solicitud
from utils.time import get_date

class SolicitudController:

    def create_solicitud(self, solicitud: Solicitud):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            query = """
                INSERT INTO solicitud (
                    id_usuario,
                    id_habitacion,
                    descripcion,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                solicitud.id_usuario,
                solicitud.id_habitacion,
                solicitud.descripcion,
                solicitud.estado,
                date,
                date
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()["id_solicitud"]
            conn.commit()

            return {
                "success": True,
                "message": "Solicitud creada correctamente.",
                "id_solicitud": new_id
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

    def get_solicitudes(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("SELECT * FROM solicitud")

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay solicitudes registradas.")

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

    def get_solicitud_id(self, id_solicitud: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT * FROM solicitud 
                WHERE id_solicitud = %s
            """, (id_solicitud,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

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

    def get_solicitudes_usuario(self, payload: dict):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            id_usuario = payload.get("id_usuario")


            cursor.execute("""
                SELECT *
                FROM solicitud
                WHERE id_usuario = %s
                ORDER BY date_created DESC
            """, (id_usuario,))

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay solicitudes para este usuario.")

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

    def create_solicitud_habitacion(self, id_usuario: int, numero_habitacion: str, descripcion: str, estado: bool = True):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            date = get_date()

            cursor.execute("SELECT id_habitacion FROM habitacion WHERE numero = %s", (numero_habitacion,))
            habitacion = cursor.fetchone()

            if not habitacion:
                raise HTTPException(status_code=404, detail=f"Habitación con número {numero_habitacion} no encontrada.")

            id_habitacion = habitacion["id_habitacion"]

            query = """
                INSERT INTO solicitud (
                    id_usuario,
                    id_habitacion,
                    descripcion,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                id_usuario,
                id_habitacion,
                descripcion,
                estado,
                date,
                date
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()["id_solicitud"]
            conn.commit()

            return {
                "success": True,
                "message": "Solicitud creada correctamente.",
                "id_solicitud": new_id
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

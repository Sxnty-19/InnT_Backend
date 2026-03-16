import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor
from config.neonConfig import connection_neon
from utils.time import get_date
from models.reserva import Reserva

class ReservaController:

    def create_reserva(self, reserva: Reserva):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            query = """
                INSERT INTO reserva (
                    id_usuario,
                    date_start,
                    date_end,
                    tiene_ninos,
                    tiene_mascotas,
                    total_cop,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_reserva;
            """
            values = (
                reserva.id_usuario,
                reserva.date_start,
                reserva.date_end,
                reserva.tiene_ninos,
                reserva.tiene_mascotas,
                reserva.total_cop,
                reserva.estado,
                date,
                date
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()["id_reserva"]
            conn.commit()

            return {
                "success": True,
                "message": "Reserva creada correctamente.",
                "id_reserva": new_id
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

    def get_reservas(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("SELECT * FROM reserva")

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay reservas registradas.")

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

    def get_reserva_id(self, id_reserva: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM reserva
                WHERE id_reserva = %s
            """, (id_reserva,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Reserva no encontrada.")

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

    def get_reservas_activas(self, id_usuario: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            cursor.execute("""
                SELECT *
                FROM reserva
                WHERE id_usuario = %s
                AND estado = TRUE
                AND (date_start > %s OR date_end > %s)
                ORDER BY date_start DESC
            """, (id_usuario, date, date))

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay reservas activas para este usuario.")
            
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

    def get_reservas_terminadas(self, id_usuario: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            cursor.execute("""
                SELECT *
                FROM reserva
                WHERE id_usuario = %s
                AND estado = TRUE
                AND date_end < %s
                ORDER BY date_end DESC
            """, (id_usuario, date, date))

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay reservas terminadas para este usuario.")
            
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

    #def get_reservas_usuarios(self):
        #

    #def delete_reserva(self, id_reserva: int):
        #

    #def create_reserva_habitaciones(self, id_usuario: int, date_start: str, date_end: str, habitaciones: list, estado=True):
        #

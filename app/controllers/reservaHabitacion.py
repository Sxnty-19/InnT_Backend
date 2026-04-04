import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor
from config.neonConfig import connection_neon
from models.reservaHabitacion import ReservaHabitacion
from utils.time import get_date

class ReservaHabitacionController:

    def create_reservaHabitacion(self, reserva_habitacion: ReservaHabitacion):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            query = """
                INSERT INTO reserva_habitacion (
                    id_reserva,
                    id_habitacion,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_rxh;
            """
            values = (
                reserva_habitacion.id_reserva,
                reserva_habitacion.id_habitacion,
                reserva_habitacion.estado,
                date,
                date
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()['id_rxh']
            conn.commit()

            return {
                "success": True,
                "message": "Reserva-Habitación creada correctamente.",
                "id_rxh": new_id
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

    def get_reservaHabitaciones(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("SELECT * FROM reserva_habitacion")

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay relaciones reserva-habitación registradas.")

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

    def get_reservaHabitacion_id(self, id_rxh: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT * FROM reserva_habitacion
                WHERE id_rxh = %s
            """, (id_rxh,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Relación reserva-habitación no encontrada.")

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

import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor
from config.neonConfig import connection_neon
from models.habitacion import Habitacion
from utils.time import get_date

class HabitacionController:

    def create_habitacion(self, habitacion: Habitacion):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            query = """
                INSERT INTO habitacion (
                    id_thabitacion,
                    numero,
                    limpieza,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_habitacion
            """
            values = (
                habitacion.id_thabitacion,
                habitacion.numero,
                habitacion.limpieza,
                habitacion.estado,
                date,
                date
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()["id_habitacion"]
            conn.commit()

            return {
                "success": True,
                "message": "Habitación creada correctamente.",
                "id_habitacion": new_id
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

    def get_habitaciones(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("SELECT * FROM habitacion")

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay habitaciones registradas.")

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

    def get_habitacion_id(self, id_habitacion: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT * FROM habitacion
                WHERE id_habitacion = %s
            """, (id_habitacion,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Habitación no encontrada.")

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

    def get_disponibles(self, date_start: str, date_end: str):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            if date_start >= date_end:
                raise HTTPException(status_code=400, detail="La fecha de inicio debe ser menor que la fecha final.")

            cursor.execute("""
                SELECT 
                    h.id_habitacion,
                    h.numero,
                    th.nombre AS tipo_habitacion,
                    th.capacidad_max,
                    th.precio_x_dia
                FROM habitacion h
                INNER JOIN tipo_habitacion th
                    ON h.id_thabitacion = th.id_thabitacion
                WHERE h.estado = TRUE
                AND NOT EXISTS (
                    SELECT 1
                    FROM reserva_habitacion rh
                    JOIN reserva r ON rh.id_reserva = r.id_reserva
                    WHERE rh.id_habitacion = h.id_habitacion
                    AND r.estado = TRUE
                    AND r.date_start < %s
                    AND r.date_end > %s
                ) 
                ORDER BY h.numero ASC
            """, (date_end, date_start))

            data = cursor.fetchall()

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

    def update_limpieza(self, id_habitacion: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            fecha_actual = get_date()

            cursor.execute("""
                SELECT limpieza FROM habitacion 
                WHERE id_habitacion = %s
            """,(id_habitacion,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Habitación no encontrada.")

            new_limpieza = not data["limpieza"]

            cursor.execute("""
                UPDATE habitacion
                SET limpieza = %s,
                    date_updated = %s
                WHERE id_habitacion = %s
            """, (new_limpieza, fecha_actual, id_habitacion))
            conn.commit()

            return {
                "success": True,
                "message": "Estado de limpieza actualizado."
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

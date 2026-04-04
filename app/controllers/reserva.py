import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta

from realtime import Optional
from config.neonConfig import connection_neon
from models.reserva import Reserva
from utils.time import get_date

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
                    capacidad_total,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_reserva;
            """
            values = (
                reserva.id_usuario,
                reserva.date_start,
                reserva.date_end,
                reserva.tiene_ninos,
                reserva.tiene_mascotas,
                reserva.total_cop,
                reserva.capacidad_total,
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

    def get_reservas_activas(self, payload: dict):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()
            id_usuario = payload.get("id_usuario")

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

    def get_reservas_terminadas(self, payload: dict):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()
            id_usuario = payload.get("id_usuario")

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

    def get_reservas_usuarios(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    r.date_start,
                    r.date_end,
                    r.tiene_ninos,
                    r.tiene_mascotas,
                    r.total_cop,
                    u.primer_nombre || ' ' ||
                    COALESCE(u.segundo_nombre, '') || ' ' ||
                    u.primer_apellido || ' ' ||
                    COALESCE(u.segundo_apellido, '') AS nombre_completo
                FROM reserva r
                INNER JOIN usuario u 
                    ON r.id_usuario = u.id_usuario
                WHERE r.estado = TRUE
                ORDER BY r.date_created DESC
            """)

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

    def delete_reserva(self, id_reserva: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date().replace(tzinfo=None)

            cursor.execute("""
                SELECT date_start
                FROM reserva
                WHERE id_reserva = %s
            """, (id_reserva,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Reserva no encontrada.")

            date_start = data["date_start"]

            if isinstance(date_start, str):
                try:
                    date_start = datetime.fromisoformat(date_start)
                except Exception:
                    raise HTTPException(status_code=500, detail="Formato de fecha inválido.")

            if date_start - date < timedelta(hours=24):
                raise HTTPException(status_code=400, detail="No se puede cancelar la reserva, faltan menos de 24 horas.")

            cursor.execute("""
                UPDATE reserva
                SET estado = FALSE,
                    date_updated = %s
                WHERE id_reserva = %s
            """, (date, id_reserva))

            conn.commit()

            return {
                "success": True,
                "message": "Reserva cancelada correctamente."
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

    def create_reserva_habitaciones(self, id_usuario: int, date_start: str, date_end: str, tiene_ninos: bool, tiene_mascotas: bool, habitaciones: list):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date_start = datetime.strptime(date_start, "%Y-%m-%d")
            date_end = datetime.strptime(date_end, "%Y-%m-%d")

            date = get_date()
            aux = (date_end - date_start).days
            aux_capacidad = 0
            aux_total = 0

            if date_start.date() <= date.date():
                raise HTTPException(status_code=400, detail="La fecha de inicio debe ser posterior al día actual.")

            if aux <= 0:
                raise HTTPException(status_code=400, detail="Las fechas de la reserva son inválidas.")

            cursor.execute("""
                SELECT 1 
                FROM documento 
                WHERE id_usuario = %s
            """, (id_usuario,))
            
            documento = cursor.fetchone()

            if not documento:
                raise HTTPException(status_code=400, detail="El usuario no tiene ningún documento registrado.")

            for id_h in habitaciones:
                cursor.execute("""
                    SELECT th.capacidad_max, th.precio_x_dia
                    FROM habitacion h
                    JOIN tipo_habitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
                    WHERE h.id_habitacion = %s
                """, (id_h,))

                data = cursor.fetchone()

                if not data:
                    raise HTTPException(status_code=404, detail=f"Habitación {id_h} no encontrada")

                aux_capacidad += data["capacidad_max"]
                aux_total += data["precio_x_dia"] * aux

            cursor.execute("""
                INSERT INTO reserva (
                    id_usuario, 
                    date_start, 
                    date_end,
                    tiene_ninos,
                    tiene_mascotas,
                    total_cop, 
                    capacidad_total,
                    estado, 
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_reserva
            """, (id_usuario, date_start, date_end, tiene_ninos, tiene_mascotas, aux_total, aux_capacidad, True, date, date))

            id_reserva = cursor.fetchone()["id_reserva"]

            for id_h in habitaciones:
                cursor.execute("""
                    INSERT INTO reserva_habitacion (
                        id_reserva, 
                        id_habitacion, 
                        estado, 
                        date_created, 
                        date_updated
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (id_reserva, id_h, True, date, date))

            conn.commit()

            return {
                "success": True,
                "message": "Reserva creada con habitaciones.",
                "id_reserva": id_reserva
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

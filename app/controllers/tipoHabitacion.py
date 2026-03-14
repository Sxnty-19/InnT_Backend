import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor
from config.neonConfig import connection_neon
from utils.time import get_date
from models.tipoHabitacion import TipoHabitacion

class TipoHabitacionController:

    def create_tipoHabitacion(self, tipo: TipoHabitacion):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            query = """
                INSERT INTO tipo_habitacion (
                    nombre,
                    descripcion,
                    capacidad_max,
                    precio_x_dia,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_thabitacion;
            """
            values = (
                tipo.nombre,
                tipo.descripcion,
                tipo.capacidad_max,
                tipo.precio_x_dia,
                tipo.estado,
                date,
                date
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()["id_thabitacion"]
            conn.commit()

            return {
                "success": True,
                "message": "Tipo de habitación creado correctamente.",
                "id_thabitacion": new_id
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

    def get_tiposHabitacion(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("SELECT * FROM tipo_habitacion")

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay tipos de habitación registrados.")

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

    def get_tipoHabitacion_id(self, id_thabitacion: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM tipo_habitacion
                WHERE id_thabitacion = %s
            """, (id_thabitacion,))

            data = cursor.fetchone()

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

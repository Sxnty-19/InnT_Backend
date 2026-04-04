import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor
from config.neonConfig import connection_neon
from models.usuarioHabitacion import UsuarioHabitacion
from utils.time import get_date

class UsuarioHabitacionController:

    def create_usuarioHabitacion(self, usuario_habitacion: UsuarioHabitacion):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            query = """
                INSERT INTO usuario_habitacion (
                    id_usuario,
                    id_habitacion,
                    id_reserva,
                    date_check_in,
                    date_check_out,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_uxh
            """
            values = (
                usuario_habitacion.id_usuario,
                usuario_habitacion.id_habitacion,
                usuario_habitacion.id_reserva,
                usuario_habitacion.date_check_in,
                usuario_habitacion.date_check_out,
                usuario_habitacion.estado,
                date,
                date
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()["id_uxh"]
            conn.commit()

            return {
                "success": True,
                "message": "Usuario-Habitación creada correctamente.",
                "id_uxh": new_id
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

    def get_usuariosHabitacion(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    uh.*, 
                    u.primer_nombre, 
                    u.primer_apellido, 
                    h.numero AS numero_habitacion
                FROM usuario_habitacion uh
                JOIN usuario u ON uh.id_usuario = u.id_usuario
                JOIN habitacion h ON uh.id_habitacion = h.id_habitacion
            """)

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay asignaciones registradas.")

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

    def get_usuarioHabitacion_id(self, id_uxh: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    uh.*, 
                    u.primer_nombre, 
                    u.primer_apellido, 
                    h.numero AS numero_habitacion
                FROM usuario_habitacion uh
                JOIN usuario u ON uh.id_usuario = u.id_usuario
                JOIN habitacion h ON uh.id_habitacion = h.id_habitacion
                WHERE uh.id_uxh = %s
            """, (id_uxh,))
            
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Registro no encontrado.")

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

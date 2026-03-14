import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor
from config.neonConfig import connection_neon
from models.tipoDocumento import TipoDocumento
from utils.time import get_date

class TipoDocumentoController:

    def create_tipoDocumento(self, tipo: TipoDocumento):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            query = """
                INSERT INTO tipo_documento (
                    nombre,
                    descripcion,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_tdocumento;
            """
            values = (
                tipo.nombre,
                tipo.descripcion,
                tipo.estado,
                date,
                date
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()["id_tdocumento"]
            conn.commit()

            return {
                "success": True,
                "message": "Tipo de documento creado correctamente.",
                "id_tdocumento": new_id
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

    def get_tiposDocumento(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("SELECT * FROM tipo_documento")

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay tipos de documento registrados.")

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

    def get_tipoDocumento_id(self, id_tdocumento: int): #---
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM tipo_documento
                WHERE id_tdocumento = %s
            """, (id_tdocumento,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Tipo de documento no encontrado.")

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

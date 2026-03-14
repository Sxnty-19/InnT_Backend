import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor
from config.neonConfig import connection_neon
from models.documento import Documento
from utils.time import get_date

class DocumentoController:

    def create_documento(self, documento: Documento):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            if documento.numero_documento:
                cursor.execute(
                    "SELECT 1 FROM documento WHERE numero_documento = %s", (documento.numero_documento,)
                )
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="El número de documento ya está registrado")

            query = """
                INSERT INTO documento (
                    id_tdocumento,
                    id_usuario,
                    numero_documento,
                    lugar_expedicion,
                    url_imagen,
                    documento_validado,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_documento
            """
            values = (
                documento.id_tdocumento,
                documento.id_usuario,
                documento.numero_documento,
                documento.lugar_expedicion,
                documento.url_imagen,
                documento.documento_validado,
                documento.estado,
                date,
                date
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()["id_documento"]
            conn.commit()

            return {
                "success": True,
                "message": "Documento creado correctamente.",
                "id_documento": new_id
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

    def get_documentos(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("SELECT * FROM documento")

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay documentos registrados.")

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

    def get_documento_id(self, id_documento: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT * FROM documento
                WHERE id_documento = %s
            """, (id_documento,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Documento no encontrado.")

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

    def get_documentos_usuarios(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    d.numero_documento,
                    d.lugar_expedicion,
                    d.url_imagen,
                    d.documento_validado,
                    u.primer_nombre || ' ' ||
                    COALESCE(u.segundo_nombre, '') || ' ' ||
                    u.primer_apellido || ' ' ||
                    COALESCE(u.segundo_apellido, '') AS nombre_completo,
                    td.nombre AS tipo_documento
                FROM documento d
                INNER JOIN usuario u 
                    ON d.id_usuario = u.id_usuario
                INNER JOIN tipo_documento td
                    ON d.id_tdocumento = td.id_tdocumento
                WHERE d.estado = TRUE
                ORDER BY d.date_created DESC
            """)

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay documentos registrados.")

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

    def get_documentos_usuario(self, payload: dict):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            id_usuario = payload.get("id_usuario")

            cursor.execute("""
                SELECT
                    d.numero_documento,
                    d.lugar_expedicion,
                    d.url_imagen,
                    d.documento_validado,
                    td.nombre AS tipo_documento
                FROM documento d
                INNER JOIN tipo_documento td
                    ON d.id_tdocumento = td.id_tdocumento
                WHERE d.id_usuario = %s AND d.estado = TRUE
                ORDER BY d.date_created DESC
            """, (id_usuario,))

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay documentos registrados para este usuario.")

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

    def delete_documento(self, id_documento: int):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            date = get_date()

            cursor.execute("""
                UPDATE documento
                SET estado = FALSE,
                    date_updated = %s
                WHERE id_documento = %s
                RETURNING id_documento
            """, (date, id_documento))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Documento no encontrado.")

            conn.commit()

            return {
                "success": True,
                "message": "Documento eliminado correctamente."
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

    def get_usuario_documento(self, numero_documento: str):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    u.id_usuario,
                    u.primer_nombre || ' ' ||
                    COALESCE(u.segundo_nombre, '') || ' ' ||
                    u.primer_apellido || ' ' ||
                    COALESCE(u.segundo_apellido, '') AS nombre_completo
                FROM documento d
                INNER JOIN usuario u 
                    ON d.id_usuario = u.id_usuario
                WHERE d.numero_documento = %s
                LIMIT 1
            """, (numero_documento,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="No se encontró ningún usuario con ese número de documento.")

            return {
                "success": True,
                "message": "Usuario encontrado.",
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

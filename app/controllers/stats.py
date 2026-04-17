import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor
from config.neonConfig import connection_neon

class StatsController:

    # Indicadores

    def get_total_usuarios(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM usuario
                WHERE estado = TRUE
            """)

            data = cursor.fetchone()

            return {
                "success": True,
                "data": data["total"]
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_reservas_programadas(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM reserva
                WHERE date_start > NOW()
                AND estado = TRUE
            """)

            data = cursor.fetchone()

            return {
                "success": True,
                "data": data["total"]
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_habitaciones_disponibles(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM habitacion
                WHERE estado = TRUE
            """)

            data = cursor.fetchone()

            return {
                "success": True,
                "data": data["total"]
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_ingresos_mes(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT COALESCE(SUM(total_cop), 0) AS total
                FROM reserva
                WHERE DATE_TRUNC('month', date_created) = DATE_TRUNC('month', NOW())
            """)

            data = cursor.fetchone()

            return {
                "success": True,
                "data": float(data["total"])
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # Graficas

    def get_reservas_por_mes(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    DATE_TRUNC('month', date_created) AS mes,
                    COUNT(*) AS total
                FROM reserva
                GROUP BY mes
                ORDER BY mes
            """)

            data = cursor.fetchall()

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_ingresos_por_mes(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    DATE_TRUNC('month', date_created) AS mes,
                    COALESCE(SUM(total_cop), 0) AS ingresos
                FROM reserva
                GROUP BY mes
                ORDER BY mes
            """)

            data = cursor.fetchall()

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_tipos_habitacion(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    th.nombre,
                    COUNT(*) AS total
                FROM reserva_habitacion rh
                JOIN habitacion h ON rh.id_habitacion = h.id_habitacion
                JOIN tipo_habitacion th ON h.id_thabitacion = th.id_thabitacion
                GROUP BY th.nombre
            """)

            data = cursor.fetchall()

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_usuarios_por_rol(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    r.nombre,
                    COUNT(*) AS total
                FROM usuario u
                JOIN rol r ON u.id_rol = r.id_rol
                GROUP BY r.nombre
            """)

            data = cursor.fetchall()

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_habitaciones_por_tipo(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    th.nombre,
                    COUNT(*) AS total
                FROM habitacion h
                JOIN tipo_habitacion th ON h.id_thabitacion = th.id_thabitacion
                GROUP BY th.nombre
            """)

            data = cursor.fetchall()

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_solicitudes_por_dia(self):
        conn = None
        cursor = None

        try:
            conn = connection_neon()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    DATE(date_created) AS dia,
                    COUNT(*) AS total
                FROM solicitud
                GROUP BY dia
                ORDER BY dia
            """)

            data = cursor.fetchall()

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

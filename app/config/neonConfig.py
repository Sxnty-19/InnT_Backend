from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

def connection_neon():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        sslmode=os.getenv("PGSSLMODE")
    )

if __name__ == "__main__":
    try:
        print("Probando conexión a Neon...")
        conn = connection_neon()
        cur = conn.cursor()
        cur.execute("SELECT current_database(), current_user")
        print("Conexión exitosa:", cur.fetchone())
        conn.close()
    except psycopg2.Error as err:
        print("Conexión fallida:", err)

# db.py: Configuración de la base de datos
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="srv1851.hstgr.io",
        user="u911718531_senati",
        password="S3nati123",
        database="u911718531_moviles20251"
    )

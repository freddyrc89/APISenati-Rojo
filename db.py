# Configuración de la base de datos
import mysql.connector
import os

# Configuración de conexión a MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="api_db"
    )

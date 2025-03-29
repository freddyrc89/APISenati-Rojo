import mysql.connector
from datetime import datetime

# pa la base de datos
DATABASE_CONFIG = {
    'host': 'srv1851.hstgr.io',
    'user': 'u911718531_senati',
    'password': 'S3nati123',
    'database': 'u911718531_moviles20251',
    'port': 3306
}

# Función para conectar a la base de datos
def conectar_db():
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    return conn

# Función para insertar un invitado
def insertar_invitado(nombre, apellido, fecha_registro):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO invitados (nombre, apellido, created_at)
        VALUES (%s, %s, %s)
    """, (nombre, apellido, fecha_registro))

    conn.commit()  # Guardamos los cambios
    cursor.close()  # Cerramos el cursor
    conn.close()  # Cerramos la conexión

# Función para obtener los invitados
def obtener_invitados():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM invitados")
    invitados = cursor.fetchall()

    cursor.close()  # Cerrar el cursor
    conn.close()  # Cerrar la conexión

    return invitados
# models.py: Definición de la estructura de la base de datos
from db import get_db_connection
import mysql.connector


def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumnos")
    users = cursor.fetchall()
    conn.close()
    return users

def add_user(dni, nombre, programa_estudios, estado, observaciones):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alumnos (dni, nombre, programa_estudios, estado, observaciones) VALUES (%s, %s, %s, %s, %s)",
                (dni, nombre, programa_estudios, estado, observaciones))
    conn.commit()
    conn.close()

def update_user(id, nombre, programa_estudios, estado, observaciones):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE alumnos SET nombre=%s, programa_estudios=%s, estado=%s, observaciones=%s WHERE id=%s",
                (nombre, programa_estudios, estado, observaciones, id))
    conn.commit()
    conn.close()

def delete_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alumnos WHERE id=%s", (id,))
    conn.commit()
    conn.close()


def validate_qr_access(dni):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 1️⃣ Verificar si el alumno existe y su estado
        cursor.execute("SELECT estado FROM alumnos WHERE dni = %s", (dni,))
        alumno = cursor.fetchone()

        if not alumno:
            return {"error": "DNI no registrado"}, 400

        estado = alumno["estado"]

        # 2️⃣ Obtener el tiempo de caducidad del QR desde la configuración
        cursor.execute("SELECT tiempo_caducidad FROM configuracion LIMIT 1")
        config = cursor.fetchone()
        tiempo_caducidad = config["tiempo_caducidad"] if config else 3  # Valor por defecto: 3 min

        # 3️⃣ Determinar si el acceso es permitido o denegado
        if estado == "A":
            mensaje = "ACCESO OTORGADO"
            color = "green"
            estado_acceso = "PERMITIDO"
            observacion = None
            qr_expira = tiempo_caducidad  # Se usa el valor en la consulta SQL
        else:
            mensaje = "ALUMNO CON OBSERVACIONES, NO PUEDE INGRESAR"
            color = "red"
            estado_acceso = "DENEGADO"
            observacion = "Alumno en estado de deuda"
            qr_expira = None  # No hay expiración para accesos denegados

        # 4️⃣ Guardar el intento de acceso en la BD
        if estado_acceso == "PERMITIDO":
            cursor.execute("""
            INSERT INTO accesos (dni, estado_acceso, observaciones, qr_expira)
            VALUES (%s, %s, %s, NOW() + INTERVAL %s MINUTE)
            """, (dni, estado_acceso, observacion, qr_expira))
        else:
            cursor.execute("""
            INSERT INTO accesos (dni, estado_acceso, observaciones, qr_expira)
            VALUES (%s, %s, %s, '0000-00-00 00:00:00')
            """, (dni, estado_acceso, observacion))
        
        conn.commit()

        return {"mensaje": mensaje, "color": color, "estado": estado_acceso}

    except mysql.connector.Error as e:
        return {"error": f"Error en la base de datos: {e}"}

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()




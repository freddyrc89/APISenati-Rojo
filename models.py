# Definición de la estructura de la base de datos
from db import get_db_connection

# Función para obtener todos los usuarios
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# Función para agregar un nuevo usuario
def add_user(name, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    conn.close()
    
# Función para actualizar un usuario existente
def update_user(id, name, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, id))
    conn.commit()
    updated = cursor.rowcount  # Verifica si se actualizó alguna fila
    conn.close()
    return updated > 0  # Retorna True si se actualizó al menos un usuario

# Función para eliminar un usuario
def delete_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    deleted = cursor.rowcount  # Verifica si se eliminó alguna fila
    conn.close()
    return deleted > 0  # Retorna True si se eliminó al menos un usuario


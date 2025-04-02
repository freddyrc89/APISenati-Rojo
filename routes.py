# routes.py: Definición de las rutas de la API
from flask import Flask, jsonify, request
from models import get_users, add_user, update_user, delete_user, validate_qr_access, insertar_invitado, obtener_invitados
import mysql.connector

app = Flask(__name__)

@app.route('/alumnos', methods=['GET'])
def get_all_users():
    return jsonify(get_users())

@app.route('/alumnos', methods=['POST'])
def create_user():
    data = request.json
    add_user(data['dni'], data['nombre'], data['programa_estudios'], data['estado'], data.get('observaciones', ''))
    return jsonify({"message": "Alumno agregado"})

@app.route('/alumnos/<int:id>', methods=['PUT'])
def modify_user(id):
    data = request.json
    update_user(id, data['nombre'], data['programa_estudios'], data['estado'], data.get('observaciones', ''))
    return jsonify({"message": "Alumno actualizado"})

@app.route('/alumnos/<int:id>', methods=['DELETE'])
def remove_user(id):
    delete_user(id)
    return jsonify({"message": "Alumno eliminado"})

@app.route('/validar_qr', methods=['POST'])
def qr_access():
    data = request.json
    
    if not data or 'dni' not in data or not data['dni'].strip():
        return jsonify({"error": "El DNI es obligatorio"}), 400  # Código 400 = Bad Request

    return jsonify(validate_qr_access(data['dni']))

# Ruta para registrar invitados
@app.route('/invitado', methods=['POST'])
def registrar_invitado():
    datos = request.get_json()

    nombre = datos.get('nombre')
    apellido = datos.get('apellido')

    if not nombre or not apellido:
        return jsonify({"error": "Nombre y apellido son obligatorios"}), 400

    fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # para insertar a la base de datos
        insertar_invitado(nombre, apellido, fecha_registro)

        return jsonify({
            "mensaje": "Invitado registrado correctamente",
            "invitado": {
                "nombre": nombre,
                "apellido": apellido,
                "fecha_registro": fecha_registro
            }
        }), 201

    except mysql.connector.Error as err:
        return jsonify({"error": f"Error en la base de datos: {err}"}), 500

# Ruta para listar todos los invitados
@app.route('/invitados', methods=['GET'])
def listar_invitados():
    try:
        invitados = obtener_invitados()
        return jsonify({"invitados": invitados})

    except mysql.connector.Error as err:
        return jsonify({"error": f"Error en la base de datos: {err}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
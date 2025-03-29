import mysql.connector
from flask import Flask, request, jsonify
from datetime import datetime
from invitadosdb import insertar_invitado, obtener_invitados

app = Flask(__name__)

# Ruta de bienvenida
@app.route('/')
def home():
    return jsonify({"mensaje": "Bienvenido al Registro de Invitados"}), 200

# Ruta para registrar invitadosxd
@app.route('/invitado', methods=['POST'])
def registrar_invitado():
    datos = request.get_json()

    nombre = datos.get('nombre')
    apellido = datos.get('apellido')

    if not nombre or not apellido:
        return jsonify({"error": "Nombre y apellido son obligatorios"}), 400

    fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # para insertar a la base de datos p
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

# Ruta z listar todos los invitados
@app.route('/invitados', methods=['GET'])
def listar_invitados():
    try:
        invitados = obtener_invitados()
        return jsonify({"invitados": invitados})

    except mysql.connector.Error as err:
        return jsonify({"error": f"Error en la base de datos: {err}"}), 500


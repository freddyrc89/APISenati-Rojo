# routes.py: Definición de las rutas de la API
from flask import Flask, jsonify, request
from models import get_users, add_user, update_user, delete_user, validate_qr_access

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

if __name__ == '__main__':
    app.run(debug=True)
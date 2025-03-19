# Definición de las rutas de la API
from flask import Flask, jsonify, request
from models import get_users, add_user, update_user, delete_user  # Importa las nuevas funciones

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_all_users():
    users = get_users()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    add_user(data['name'], data['email'])
    return jsonify({"message": "Usuario agregado exitosamente"}), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_existing_user(id):
    data = request.get_json()
    
    if 'name' not in data or 'email' not in data:
        return jsonify({"error": "Faltan datos"}), 400

    updated = update_user(id, data['name'], data['email'])
    
    if updated:
        return jsonify({"message": "Usuario actualizado exitosamente"}), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_existing_user(id):
    deleted = delete_user(id)
    
    if deleted:
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)


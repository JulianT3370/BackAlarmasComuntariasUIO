from flask import Blueprint, request, jsonify, current_app

api = Blueprint("api", __name__)

# Crear un nuevo sector (POST)
@api.route("/sectores", methods=["POST"])
def crear_sector():
    data = request.json
    if not data or not data.get("nombre"):
        return jsonify({"error": "El nombre del sector es obligatorio"}), 400

    sector = {
        "nombre": data["nombre"],
        "descripcion": data.get("descripcion", ""),
        "numero_alarmas": data.get("numero_alarmas", 0)  # Campo adicional
    }

    # Acceso a MongoDB desde current_app
    current_app.mongo.db["sectores"].insert_one(sector)
    return jsonify({"message": "Sector creado con éxito"}), 201

# Obtener todos los sectores (GET)
@api.route("/sectores", methods=["GET"])
def obtener_sectores():
    # Acceso a MongoDB desde current_app
    sectores = list(current_app.mongo.db["sectores"].find({}, {"_id": 0}))
    return jsonify(sectores), 200

# Actualizar un sector (PUT)
@api.route("/sectores/<string:nombre>", methods=["PUT"])
def actualizar_sector(nombre):
    data = request.json
    if not data:
        return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

    resultado = current_app.mongo.db["sectores"].update_one(
        {"nombre": nombre},
        {"$set": {
            "descripcion": data.get("descripcion", ""),
            "numero_alarmas": data.get("numero_alarmas", 0)
        }}
    )

    if resultado.matched_count == 0:
        return jsonify({"error": "Sector no encontrado"}), 404

    return jsonify({"message": "Sector actualizado con éxito"}), 200

# Eliminar un sector (DELETE)
@api.route("/sectores/<string:nombre>", methods=["DELETE"])
def eliminar_sector(nombre):
    resultado = current_app.mongo.db["sectores"].delete_one({"nombre": nombre})

    if resultado.deleted_count == 0:
        return jsonify({"error": "Sector no encontrado"}), 404

    return jsonify({"message": "Sector eliminado con éxito"}), 200

# Activar una alarma para un sector (POST)
@api.route("/alarma", methods=["POST"])
def activar_alarma():
    data = request.json
    if not data or not data.get("sector"):
        return jsonify({"error": "El sector es obligatorio"}), 400

    # Validar si el sector existe
    sector = current_app.mongo.db["sectores"].find_one({"nombre": data["sector"]})
    if not sector:
        return jsonify({"error": f"El sector {data['sector']} no existe"}), 404

    return jsonify({"message": f"Alarma activada para el sector {data['sector']}"}), 200

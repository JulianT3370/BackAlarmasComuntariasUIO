from flask import Blueprint, request, jsonify, current_app

api = Blueprint("api", __name__)

@api.route("/sectores", methods=["POST"])
def crear_sector():
    data = request.json
    if not data.get("nombre"):
        return jsonify({"error": "El nombre del sector es obligatorio"}), 400

    sector = {"nombre": data["nombre"], "descripcion": data.get("descripcion", "")}
    current_app.db["sectores"].insert_one(sector)  # Usar current_app para acceder a la base de datos
    return jsonify({"message": "Sector creado con éxito"}), 201

@api.route("/sectores", methods=["GET"])
def obtener_sectores():
    sectores = list(current_app.db["sectores"].find({}, {"_id": 0}))  # Usar current_app para la base de datos
    return jsonify(sectores), 200

@api.route("/alarma", methods=["POST"])
def activar_alarma():
    data = request.json
    if not data.get("sector"):
        return jsonify({"error": "El sector es obligatorio"}), 400

    return jsonify({"message": f"Alarma activada para el sector {data['sector']}"}), 200

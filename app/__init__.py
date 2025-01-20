from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")  # Cargar configuración desde config.py

    # Configurar CORS
    CORS(app)

    # Conexión a MongoDB
    mongo_client = MongoClient(app.config["MONGO_URI"])
    app.db = mongo_client.get_database()  # Seleccionar la base de datos

    # Registrar rutas
    from app.routes import api
    app.register_blueprint(api)

    return app

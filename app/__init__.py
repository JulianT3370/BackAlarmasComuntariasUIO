from flask import Flask
from flask_pymongo import PyMongo
from config import Config

# Inicializar PyMongo
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar MongoDB con la aplicación
    mongo.init_app(app)

    # Registrar Blueprint
    from app.routes import api
    app.register_blueprint(api, url_prefix="/api")

    # Hacer mongo accesible globalmente usando app
    app.mongo = mongo

    return app

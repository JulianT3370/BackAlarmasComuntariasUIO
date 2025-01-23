import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Obtén el puerto de la variable de entorno (DigitalOcean lo define automáticamente)
    port = int(os.environ.get("PORT", 8080))  # Usa 8080 por defecto si no se encuentra la variable PORT
    app.run(debug=True, host="0.0.0.0", port=port)  # Asegúrate de usar host="0.0.0.0" para aceptar conexiones externas

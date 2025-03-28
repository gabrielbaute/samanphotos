"""Punto de entrada de la aplicación Flask."""

from app import create_app
from config import Config

app = create_app()

if __name__ == "__main__":
    app.run(debug=Config.DEBUG, port=Config.PORT)

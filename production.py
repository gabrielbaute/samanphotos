from app import create_app
from config import Config
from waitress import serve

app = create_app()

if __name__ == "__main__":
    serve(
        app,
        host='0.0.0.0',
        port=Config.PORT,
        ident=Config.APP_NAME
        )
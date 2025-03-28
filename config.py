"""Configuración de la aplicación Flask."""

import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env en el directorio raíz
load_dotenv()

# Función para convertir una cadena a un valor booleano
def str_to_bool(value):
    return value.lower() in ['true', '1', 'yes']

class Config:
    """Configuración de la aplicación Flask."""

    # Admin user
    ADMIN_EMAIL=os.getenv('ADMIN_EMAIL')
    ADMIN_PASSWORD=os.getenv('ADMIN_PASSWORD')
    ADMIN_USERNAME=os.getenv("ADMIN_USERNAME")

    # Flask configuration
    APP_NAME=os.getenv("APP_NAME")
    DEBUG=os.getenv("DEBUG")
    PORT=os.getenv("PORT")
    APP_VERSION="0.1.0"
    APP_LANGUAGE="es"
    
    # Database and storage configuration
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False
    UPLOAD_FOLDER=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')

    # Security configuration
    SECRET_KEY=os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT=os.getenv('SECURITY_PASSWORD_SALT')
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
    
    # Configuración de Flask-Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = str_to_bool(os.environ.get('MAIL_USE_TLS', 'False'))
    MAIL_USE_SSL = str_to_bool(os.environ.get('MAIL_USE_SSL', 'False'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_DEBUG = int(os.environ.get('MAIL_DEBUG', 0))
    CACHE_TYPE='simple'

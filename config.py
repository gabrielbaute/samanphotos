"""Configuración de la aplicación Flask."""

import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env en el directorio raíz
load_dotenv()

class Config:
    """Configuración de la aplicación Flask."""

    # Admin user
    ADMIN_EMAIL=os.getenv('ADMIN_EMAIL')
    ADMIN_PASSWORD=os.getenv('ADMIN_PASSWORD')
    ADMIN_USERNAME=os.getenv("ADMIN_USERNAME")

    # Flask configuration
    APP_NAME=os.getenv("APP_NAME")
    PORT=os.getenv("PORT")
    APP_VERSION="0.1.0"
    APP_LANGUAGE="es"
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///db.sqlite3'
    UPLOAD_FOLDER=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')

    # Security configuration
    SECRET_KEY=os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT=os.getenv('SECURITY_PASSWORD_SALT')
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
    
    # Flask Mail configuration
    MAIL_SERVER=os.getenv('MAIL_SERVER')
    MAIL_PORT=os.getenv('MAIL_PORT')
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS')
    MAIL_USE_SSL=os.getenv('MAIL_USE_SSL')
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
    CACHE_TYPE='simple'

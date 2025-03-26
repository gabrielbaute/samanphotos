import os
import logging
from logging.handlers import RotatingFileHandler
from config import Config

server_name = Config.APP_NAME

def setup_logging(app):
    """
    Configura el logging para la aplicación Flask.
    """
    
    # Configuración de logging
    log_directory = 'logs'
    log_file = os.path.join(log_directory, f'{server_name}.log')

    # Crear el directorio si no existe
    os.makedirs(log_directory, exist_ok=True)

    # Configurar el RotatingFileHandler
    file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        f'[({server_name})] %(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)

    # Agregar el manejador al logger de Flask
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    # Mensaje de inicio
    app.logger.info(f'{server_name} inicializada correctamente')

    # Imprimir la ruta del archivo de log
    app.logger.info(f'Archivo de log creado en: {os.path.abspath(log_file)}')
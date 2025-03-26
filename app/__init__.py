"""Modulo de inicialización de la aplicación Flask"""

import os

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_login import current_user

from app.extensions import mail, login_manager, cache, jwt
from database.models import User
from database.db_config import db, init_db
from app.routes import register_blueprints
from core.samanapi import api_bp
from utils import create_admin_user
from config import Config




def create_app():
    """Crea una instancia de la aplicación Flask"""
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    
    # Set config variables
    app.config.from_object(Config)

    # Initialize components
    init_db(app)
    mail.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    cache.init_app(app)
    jwt.init_app(app)

    # Blueprints register
    register_blueprints(app)
    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()
        create_admin_user()

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    
    
    @app.context_processor
    def inject_app_name():
        return {
            "app_name": app.config["APP_NAME"],
            "app_version": app.config["APP_VERSION"],
            "app_language": app.config["APP_LANGUAGE"]
            }
    
    return app


@login_manager.user_loader
def load_user(user_id):
    """Cargar un usuario por ID
    Args:
        user_id (int): ID del usuario
    Returns:
        User: Objeto de usuario
    """
    return User.query.get(int(user_id))

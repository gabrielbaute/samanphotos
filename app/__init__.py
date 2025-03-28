"""Modulo de inicialización de la aplicación Flask"""

import os

from flask import Flask
from flask_migrate import Migrate

from app.extensions import login_manager, cache, jwt
from database.models import User
from database.db_config import db, init_db
from app.routes import register_blueprints
from core.samanapi import api_bp
from mail.config_mail import mail
from utils import create_admin_user, setup_logging
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
    setup_logging(app)
    mail.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    cache.init_app(app)
    jwt.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Blueprints register
    register_blueprints(app)
    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()
        create_admin_user()
        app.logger.info(f"Server listening on port: {Config.PORT}")

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

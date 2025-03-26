"""Modulo de inicialización de la aplicación Flask"""

import os
import uuid

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin
from flask_migrate import Migrate
from flask_restful import Api
from flask_caching import Cache
from flask_login import LoginManager, current_user
from flask_jwt_extended import JWTManager
from datetime import datetime

from app.extensions import mail, login_manager
from database.models import User, Role
from database.db_config import db
from app.routes import register_blueprints
from core.samanapi import api_bp
from utils import create_admin_user

cache=Cache()
jwt=JWTManager()


def create_app():
    """Crea una instancia de la aplicación Flask"""
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object("config.Config")

    with app.app_context():
        db.init_app(app)
        mail.init_app(app)
        migrate = Migrate(app, db)
        admin = Admin(app)
        cache.init_app(app)
        login_manager.init_app(app)
        jwt.init_app(app)

        login_manager.login_view = "main.login"

        # Registrar rutas personalizadas
        register_blueprints(app)

        # Inicializar Flask-Security después de registrar rutas personalizadas
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security = Security()
        security.init_app(app, datastore=user_datastore, register_blueprint=False)

        db.create_all()
        create_admin_user()

        @app.before_request
        def update_last_login():
            if current_user.is_authenticated:
                current_user.last_login_at = current_user.current_login_at
                current_user.last_login_ip = current_user.current_login_ip
                current_user.current_login_at = datetime.utcnow()
                current_user.current_login_ip = request.remote_addr
                current_user.login_count += 1
                db.session.commit()

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    app.register_blueprint(api_bp, url_prefix='/api')
    
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

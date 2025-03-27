import uuid
from flask import current_app
from werkzeug.security import generate_password_hash

from config import Config
from utils.storage_id import generate_storage_user_id
from core.storage import create_user_storage
from database.models import User
from database.db_config import db


def create_admin_user():
    """Crear un usuario administrador si no existe"""
    admin_email = Config.ADMIN_EMAIL
    admin_password = Config.ADMIN_PASSWORD
    admin_username = Config.ADMIN_USERNAME

    try:
        if not User.query.filter_by(email=admin_email).first():
            
            hashed_password = generate_password_hash(admin_password)
            storage_user_id = generate_storage_user_id()

            storage_path = create_user_storage(storage_user_id)

            admin = User(
                username=admin_username,
                email=admin_email,
                password=hashed_password,
                role='admin',
                storage_path=storage_path,
                is_active=True)
            
            db.session.add(admin)
            db.session.commit()
        else:
            current_app.logger.info("Usuario admin ya registrado.")
    
    except Exception as e:
        current_app.logger.error(f"Error al crear el usuario admin: {e}")
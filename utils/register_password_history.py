from database.models import PasswordHistory
from database import db
from flask import current_app

def register_password_history_event(user):
    """Registrar el historial de contraseñas de un usuario"""
    try:
        # Registrar el cambio de contraseña
        new_password_history = PasswordHistory(user_id=user.id, password_hash=user.password)
        db.session.add(new_password_history)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error al registrar el historial de contraseñas: {e}")
        db.session.rollback()
        return False
    return True
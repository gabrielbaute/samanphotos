from flask import current_app
from database import db
from database.models import SessionHistory

def register_session_event(user, request):
    """Registrar un evento de sesión en la base de datos"""
    try:
        # Registrar el evento de inicio de sesión
        session_event = SessionHistory(
            usuario_id=user.id,
            tipo_evento='LOGIN',
            ip_origen=request.remote_addr,
            dispositivo=request.user_agent.platform,
            navegador=request.user_agent.browser
        )
        db.session.add(session_event)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error al registrar el evento de sesión: {e}")
        db.session.rollback()
        return False
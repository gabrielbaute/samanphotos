from flask import request, current_app
from database import db
from database.models import AuditLog

def registrar_auditoria(usuario_id, accion, detalles=None):
    # Validar y establecer valores por defecto
    ip_origen = request.remote_addr or "Unknown"
    dispositivo = request.user_agent.platform or "Unknown"
    user_agent = request.headers.get('User-Agent') or "Unknown"

    try:
        audit_log = AuditLog(
            usuario_id=usuario_id,
            accion=accion,
            detalles=detalles,
            ip_origen=ip_origen,
            dispositivo=dispositivo,
            user_agent=user_agent,
        )
        db.session.add(audit_log)
        db.session.commit()

        current_app.logger.info(f"Nueva acción registrada en auditoria: {accion}")
    except Exception as e:
        current_app.logger.error(f"Error al registrar auditoria: {e}")
        db.session.rollback()
        return False
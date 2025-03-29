import os
from database.models import SessionHistory, AuditLog, User, Album, Photo
from utils.admin_utils import get_user_storage
from flask_login import current_user

def get_sessions_user_history(usuario_id):
    """
    Obtiene el historial de sesiones del usuario dado su ID.
    """
    sesiones = SessionHistory.query.filter_by(usuario_id=usuario_id).order_by(SessionHistory.fecha_evento.desc()).all()
    return [
        {
            "fecha_evento": sesion.fecha_evento.strftime('%d-%m-%Y %H:%M:%S'),
            "ip_origen": sesion.ip_origen,
            "dispositivo": sesion.dispositivo or "Desconocido",
            "navegador": sesion.navegador or "Desconocido"
        }
        for sesion in sesiones
    ]

def get_auditlog_user(usuario_id):
    """
    Obtiene el registro de actividad del usuario dado su ID.
    """
    registros = AuditLog.query.filter_by(usuario_id=usuario_id).order_by(AuditLog.fecha_cambio.desc()).all()
    return [
        {
            "fecha_cambio": registro.fecha_cambio.strftime('%d-%m-%Y %H:%M:%S'),
            "accion": registro.accion,
            "detalles": registro.detalles or "Sin detalles",
            "ip_origen": registro.ip_origen,
            "dispositivo": registro.dispositivo or "Desconocido",
            "observaciones": registro.observaciones or "Sin observaciones"
        }
        for registro in registros
    ]



def get_user_data(user):
    """
    Obtiene información crítica del usuario.
    """
    # Convierte a MB
    storage_used_mb = get_user_storage(user)

    # Cuenta los álbumes y fotos
    albums_count = Album.query.filter_by(user_id=user.id).count()
    fotos_count = Photo.query.filter_by(user_id=user.id).count()

    user_data = {
        "storage_used_mb": storage_used_mb,
        "albums_count": albums_count,
        "fotos_count": fotos_count,
        "foto_perfil": user.foto_perfil,
        "username": user.username,
        "email": user.email,
        "fecha_nacimiento": user.fecha_nacimiento if user.fecha_nacimiento else "Desconocida",
        "fecha_registro": user.created_at.strftime('%d-%m-%Y') if user.created_at else "Desconocida"
        }

    return user_data
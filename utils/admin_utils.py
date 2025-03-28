import os
from datetime import datetime
from config import Config
from database.models import User, SessionHistory

def get_logs():
    """
    Obtiene la lista de archivos .log en el directorio logs.
    """
    log_directory = 'logs'
    log_files = [f for f in os.listdir(log_directory) if f.endswith('.log')]
    if not log_files:
        return ['No se encontraron archivos de log.']
    
    logs = {}
    for log_file in log_files:
        file_path = os.path.join(log_directory, log_file)
        with open(file_path, 'r') as f:
            logs[log_file] = f.readlines()
    return logs

def get_app_log():
    """
    Obtiene el contenido del archivo de log basado en Config.APP_NAME.
    """
    log_directory = 'logs'
    log_file = os.path.join(log_directory, f'{Config.APP_NAME}.log')
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            return f.readlines()
    return ['No se encontró el archivo de log']

def get_user_storage(user):
    user_folder = user.storage_path  # Asumiendo que el modelo User tiene un campo storage_path
    if not os.path.exists(user_folder):
        return 0  # Si la carpeta no existe, devuelve 0 MB
    size = sum(os.path.getsize(os.path.join(user_folder, file)) for file in os.listdir(user_folder))
    return round(size / (1024 * 1024), 2)  # Convertir a MB


def get_stats():
    users = User.query.all()
    user_stats = [
        {
            'username': user.username,
            'is_active': user.is_active,
            'session_count': SessionHistory.query.filter_by(usuario_id=user.id).count(),
            'last_connection': max([session.fecha_evento for session in SessionHistory.query.filter_by(usuario_id=user.id)]).strftime('%d-%m-%Y %H:%M:%S'),
            'mbs_used': get_user_storage(user)
        } for user in users
    ]
    print(user_stats)
    return user_stats

def is_admin(user):
    """Verifica si el usuario es administrador."""
    if user.role != 'admin':
        return False
    else:
        return True
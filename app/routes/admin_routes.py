"""Rutas para admin."""

import os

from flask import Blueprint, redirect, render_template, url_for, flash, request
from flask_login import login_required, current_user
from database.db_config import db
from database.models import User, SessionHistory

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
def admin_dashboard():
    # Verifica si el usuario tiene permisos de administrador
    if current_user.role != 'admin':
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('public.index'))

    # Renderiza la plantilla base con tabs
    return render_template('admin/dashboard.html')

@admin.route('/logs')
@login_required
def admin_logs():
    # Ejemplo de lectura del log del administrador
    log_path = os.path.join('path_a_log', 'admin.log')  # Ruta al archivo de log
    try:
        with open(log_path, 'r') as f:
            log_data = f.readlines()
    except FileNotFoundError:
        log_data = ['No se encontró el archivo de log']
    return render_template('admin/logs.html', log_data=log_data)

@admin.route('/stats')
@login_required
def admin_stats():
    # Ejemplo de extracción de estadísticas de usuarios
    users = User.query.all()
    user_stats = [
        {
            'username': user.username,
            'is_active': user.is_active,
            'session_count': SessionHistory.query.filter_by(usuario_id=user.id).count(),
            'last_connection': max([session.fecha_evento for session in SessionHistory.query.filter_by(usuario_id=user.id)]),
            'mbs_used': get_user_storage(user.storage_path)  # Implementa una función para calcular esto
        } for user in users
    ]
    return render_template('admin/stats.html', user_stats=user_stats)

def get_user_storage(user_folder):
    # Ejemplo básico de cálculo de espacio ocupado
    user_folder = user_folder
    size = sum(os.path.getsize(os.path.join(user_folder, file)) for file in os.listdir(user_folder))
    return round(size / (1024 * 1024), 2)  # Convierte a MB
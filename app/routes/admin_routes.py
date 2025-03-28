"""Rutas para admin."""

import os

from flask import Blueprint, redirect, render_template, url_for, flash, request
from flask_login import login_required, current_user
from config import Config
from utils import get_logs, get_stats, is_admin
from database.db_config import db
from database.models import User, SessionHistory

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
def admin_dashboard():
    # Verifica si el usuario tiene permisos de administrador
    admin = is_admin(current_user)
    if not admin:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('public.index'))

    # Renderiza la plantilla base con tabs
    return render_template('admin/dashboard.html')

@admin.route('/logs')
@login_required
def admin_logs():
    # Verifica si el usuario tiene permisos de administrador
    admin = is_admin(current_user)
    if not admin:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('public.index'))
    
    logs = get_logs()

    return render_template('admin/logs.html', logs=logs)

@admin.route('/stats')
@login_required
def admin_stats():
    # Verifica si el usuario tiene permisos de administrador
    admin = is_admin(current_user)
    if not admin:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('public.index'))
    
    user_stats = get_stats()
    
    return render_template('admin/stats.html', stats=user_stats)
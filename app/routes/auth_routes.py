"""Rutas de autenticación de usuarios"""

import uuid

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from database.db_config import db
from database.models import User
from app.forms import LoginForm, RegisterForm, ResetPasswordForm
from core import create_user_storage
from core.mail import send_reset_email

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Ruta de inicio de sesión"""
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    
    if form.validate_on_submit():
        try:     
            user = User.query.filter_by(email=form.email.data).first()
        
            if not user:
                flash('Por favor verifique sus datos de inicio de sesión y vuelva a intentarlo.', 'danger')
                return redirect(url_for('auth.login'))

        
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful', 'success')
                return redirect(url_for("photos.profile"))            
            else:
                flash("Usuario o contraseña inválidos")
        except Exception as e:
            current_app.logger.error(f"Error al intentar autenticar: {e}")
    return render_template("login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    """Ruta de cierre de sesión"""
    logout_user()
    return redirect(url_for("public.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Ruta de registro de usuario"""
    form = RegisterForm()
    if form.validate_on_submit():
        # Crear el usuario y su ruta de almacenamiento
        storage_user_id = uuid.uuid4().hex
        storage_path = create_user_storage(storage_user_id)
        password_hash = generate_password_hash(form.password.data)
        new_user = User(
            email=form.email.data,
            username=form.username.data,
            password=password_hash,
            storage_path=storage_path,
        )
        db.session.add(new_user)
        db.session.commit()

        # Iniciar sesión del nuevo usuario
        login_user(new_user)
        return redirect(url_for("photos.profile"))
    return render_template("register.html", form=form)


@auth.route("/resset_password", methods=["GET", "POST"])
def resset_password():
    """Ruta de restablecimiento de contraseña"""
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash(
                "Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña."
            )
            return redirect(url_for("auth.login"))
        else:
            flash("No se encontró ninguna cuenta con ese correo electrónico.")
    return render_template("resset_password.html", form=form)

"""Rutas de autenticación de usuarios"""

import uuid

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required

from app import db
from database.models import User
from app.forms import LoginForm, RegisterForm, RestorePasswordForm
from core.storage import create_user_storage
from core.mail import send_reset_email

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Ruta de inicio de sesión"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("photos.profile"))
        else:
            flash("Usuario o contraseña inválidos")
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
        new_user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
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
    form = RestorePasswordForm()
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

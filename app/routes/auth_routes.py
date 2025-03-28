"""Rutas de autenticación de usuarios"""

import uuid, json

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from database.db_config import db
from database.models import User
from app.forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm, ResendConfirmationForm
from core import create_user_storage
from utils import register_session_event, registrar_auditoria, register_password_history_event, ACCIONES
from mail import(
    send_reset_password_email,
    send_login_notification,
    send_welcome_email,
    send_account_activation_email,
    send_confirmation_email, 
    send_password_change_notification,
    decode_email_token,
    decode_reset_token
    )

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
                send_login_notification(user, request.remote_addr)
                register_session_event(user, request)
                flash('Login successful', 'success')
                return redirect(url_for("photos.profile")) 
            else:
                flash("Usuario o contraseña inválidos")
        except Exception as e:
            current_app.logger.error(f"Error al intentar autenticar: {e}")
    return render_template("auth/login.html", form=form)


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
        email=form.email.data
        username=form.username.data
        storage_user_id = uuid.uuid4().hex
        storage_path = create_user_storage(storage_user_id)
        password_hash = generate_password_hash(form.password.data)
        
        new_user = User(
            email=email,
            username=username,
            password=password_hash,
            storage_path=storage_path,
        )
        db.session.add(new_user)
        db.session.commit()
        
        
        send_welcome_email(new_user)
        
        send_confirmation_email(new_user)
        # Iniciar sesión del nuevo usuario
        
        return redirect(url_for("public.index"))
    return render_template("auth/register.html", form=form)

@auth.route('/confirm/<token>')
def confirm_email(token):
    user_id = decode_email_token(token)
    if user_id is None:
        flash('The confirmation link is invalid or has expired. Please request a new confirmation link below.', 'danger')
        return redirect(url_for('auth.resend_confirmation'))

    user = User.query.get(user_id)
    if user.is_active:
        flash('Account already confirmed. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    # Activar la cuenta del usuario
    user.is_active = True

    # Registrar la contraseña inicial en el historial
    register_password_history_event(user)

    # Registrar la acción de habilitar la cuenta
    registrar_auditoria(
        usuario_id=user.id,
        accion=ACCIONES["ACTIVACION"],
        detalles=json.dumps({
            "ip_origen": request.remote_addr,
            "dispositivo": request.user_agent.platform,
            "user_agent": request.headers.get('User-Agent')
        }),
    )
    
    db.session.commit()
    # Enviar correo de activación exitosa
    send_account_activation_email(user)

    flash('Your account has been confirmed. You can now log in.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/resend_confirmation', methods=['GET', 'POST'])
def resend_confirmation():
    form = ResendConfirmationForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if user and not user.is_active:
            send_confirmation_email(user)
            flash('Se ha enviado un nuevo mensaje de confirmación a su dirección de correo electrónico.', 'success')
        else:
            flash('Correo electrónico no válido o la cuenta ya está activa.', 'danger')

        return redirect(url_for('auth.login'))

    return render_template('auth/resend_confirmation.html', form=form)

@auth.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    """Ruta de restablecimiento de contraseña"""
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_password_email(user)
            flash(
                "Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña."
            )
            return redirect(url_for("auth.login"))
        else:
            flash("No se encontró ninguna cuenta con ese correo electrónico.")
    return render_template("auth/forgot_password.html", form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        user_id = decode_reset_token(token)
    except:
        flash('El enlace de restablecimiento no es válido o ha expirado.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        user = User.query.get(user_id)

        # Actualizar la contraseña del usuario
        user.password = generate_password_hash(password, method='pbkdf2:sha256')
        register_password_history_event(user)
        
        # **Registrar la acción en la auditoría**
        registrar_auditoria(
            usuario_id=user.id,
            accion=ACCIONES["CAMBIO_CONTRASENA"],
            detalles=json.dumps({
                "ip_origen": request.remote_addr,
                "dispositivo": request.user_agent.platform,
                "user_agent": request.headers.get('User-Agent'),
            }),
        )

        db.session.commit()
        send_password_change_notification(user, request.remote_addr)
        flash('Su contraseña ha sido restablecida. Ya puede iniciar sesión.', 'success')

        current_app.logger.info(f"El usuario {user.email} ha cambiado su contraseña exitosamente")

        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)
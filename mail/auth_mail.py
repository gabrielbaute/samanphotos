from flask_mail import Message
from flask import render_template
from datetime import datetime, timedelta
import logging, random

from mail.config_mail import mail
from mail.tokens_mail_generator import create_email_token, create_reset_token
from database.models import VerificationCode
from database import db

def send_confirmation_email(user):
    """
    Envía un email de confirmación al usuario.
    """
    try:
        token = create_email_token(user.id)
        msg = Message('Confirm Your Email', recipients=[user.email])
        msg.html = render_template('mail/confirm_email.html', username=user.username, token=token)
        mail.send(msg)
        
        logging.info(f"Confirmation email sent to {user.email}.")
    
    except Exception as e:
        logging.error(f"Failed to send confirmation email to {user.email}: {e}")

def send_reset_password_email(user):
    """
    Envía un email al usuario con un enlace para restablecer su contraseña.
    """
    try:

        token = create_reset_token(user.id)
        msg = Message('Reset Your Password', recipients=[user.email])
        msg.html = render_template('mail/reset_password.html', username=user.username, token=token)
        mail.send(msg)
        
        logging.info(f"Reset password email sent to {user.email}.")

    except Exception as e:
        logging.error(f"Failed to send reset password email to {user.email}: {e}")    

def send_account_locked_email(user):
    """
    Envía un correo al usuario cuando su cuenta ha sido bloqueada.
    """
    try:
        msg = Message('Your Account Has Been Locked', recipients=[user.email])
        msg.html = render_template('mail/account_locked_email.html', username=user.username)
        mail.send(msg)

        logging.info(f"Account locked email sent to {user.email}.")
    
    except Exception as e:
        logging.error(f"Failed to send account locked email to {user.email}: {e}")

def send_verification_code(user):
    """
    Envía un correo al usuario con un código de 6 dígitos para validación de operaciones.
    """
    try:
        # Generar un código de 6 dígitos
        code = f"{random.randint(100000, 999999)}"

        # Almacenar el código en la base de datos con un tiempo de expiración
        verification_code = VerificationCode(
            user_id=user.id,
            code=code,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        db.session.add(verification_code)
        db.session.commit()

        # Renderizar el correo con la plantilla
        msg = Message("Your Verification Code", recipients=[user.email])
        msg.html = render_template(
            'mail/verification_code_email.html',
            username=user.username,
            verification_code=code
        )
        mail.send(msg)

        logging.info(f"Verification code sent to {user.email}.")
        return code
    
    except Exception as e:
        logging.error(f"Failed to send verification code to {user.email}: {e}")
        return None
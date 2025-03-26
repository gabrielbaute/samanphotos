from flask_mail import Message
from database.models import User
from mail.config_mail import mail
from flask import request, render_template
import logging

def send_login_notification(user, ip_address):
    try:
        """
        Envía una notificación por email al usuario cuando inicia sesión en un dispositivo.
        """
        device = request.user_agent.platform
        browser = request.user_agent.browser

        # Renderizar la plantilla con los datos
        msg = Message('New Login Notification', recipients=[user.email])
        msg.html = render_template(
            'mail/login_notification.html',
            username=user.username,
            ip_address=ip_address,
            device=device,
            browser=browser
        )
        mail.send(msg)

        logging.info(f"Login notification email sent to {user.email} from IP {ip_address} via {device}/{browser}.")

    except Exception as e:
        logging.error(f"Failed to send login notification email to {user.email}: {e}")

def send_enable_2fa_notification(user):
    try:
        """
        Envía una notificación por email al usuario cuando habilita el 2FA.
        """
        ip_origen = request.remote_addr or "Unknown"
        dispositivo = request.user_agent.platform or "Unknown"
        user_agent = request.headers.get('User-Agent') or "Unknown"

        # Configurar el mensaje
        msg = Message(
            subject="Two-Factor Authentication Enabled",
            recipients=[user.email]
        )
        msg.html = render_template(
            "mail/enable_2fa_notification.html",
            username=user.username,
            ip_origen=ip_origen,
            dispositivo=dispositivo,
            user_agent=user_agent
        )
        mail.send(msg)

        logging.info(f"2FA enable notification email sent to {user.email} from IP {ip_origen} via {dispositivo}.")
    except Exception as e:
        logging.error(f"Failed to send 2FA enable notification email to {user.email}: {e}")

def send_disable_2fa_notification(user):
    try:
        """
        Envía una notificación por email al usuario cuando deshabilita el 2FA.
        """
        ip_origen = request.remote_addr or "Unknown"
        dispositivo = request.user_agent.platform or "Unknown"
        user_agent = request.headers.get('User-Agent') or "Unknown"

        # Configurar el mensaje
        msg = Message(
            subject="Two-Factor Authentication Disabled",
            recipients=[user.email]
        )
        msg.html = render_template(
            "mail/disable_2fa_notification.html",
            username=user.username,
            ip_origen=ip_origen,
            dispositivo=dispositivo,
            user_agent=user_agent
        )
        mail.send(msg)

        logging.info(f"2FA disable notification email sent to {user.email} from IP {ip_origen} via {dispositivo}.")
    except Exception as e:
         logging.error(f"Failed to send 2FA disable notification email to {user.email}: {e}")

def send_welcome_email(user):
    try:
        """
        Envía un correo de bienvenida al usuario después de crear su cuenta.
        """
        # Configurar el mensaje
        msg = Message(
            subject="Welcome to [YourAppName]!",
            recipients=[user.email]
        )
        msg.html = render_template(
            "mail/welcome_email.html",
            username=user.username
        )
        mail.send(msg)

        logging.info(f"Welcome email sent to {user.email}.")

    except Exception as e:
        logging.error(f"Failed to welcome email to {user.email}: {e}")

def send_account_activation_email(user):
    try:
        """
        Envía un correo al usuario después de que active su cuenta con éxito.
        """
        # Configurar el mensaje
        msg = Message(
            subject="Your account has been activated!",
            recipients=[user.email]
        )
        msg.html = render_template(
            "mail/account_activation_email.html",
            username=user.username
        )
        mail.send(msg)

        logging.info(f"Activation account email sent to {user.email}.")

    except Exception as e:
        logging.error(f"Failed to sent activation email to {user.email}: {e}.")

def send_password_change_notification(user, ip_address):
    try:
        """
        Envía una notificación por email al usuario cuando se detecta que la contraseña ha sido cambiada.
        """
        device = request.user_agent.platform
        browser = request.user_agent.browser

        # Renderizar la plantilla con los datos
        msg = Message('Your password has been changed', recipients=[user.email])
        msg.html = render_template(
            'mail/password_changed_notification.html',
            username=user.username,
            ip_address=ip_address,
            device=device,
            browser=browser
        )
        mail.send(msg)

        logging.info(f"Password change notification email sent to {user.email} from IP {ip_address} via {device}/{browser}.")
    
    except Exception as e:
        logging.error(f"Failed to send password change notification email to {user.email} from IP {ip_address} via {device}.: {e}")
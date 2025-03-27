"""Rutas públicas de la aplicación."""

from flask import Blueprint, render_template, current_app
from flask_mail import Message, Mail
from mail.config_mail import mail

public = Blueprint("public", __name__)


@public.route("/")
def index():
    """Ruta principal de la aplicación."""
    return render_template("index.html")


@public.route('/test-mail')
def test_mail():
    try:
        # Verificación de configuración REAL usada
        print("\n=== CONFIGURACIÓN REAL ===")
        print(f"MAIL_SERVER: {current_app.extensions['mail'].server}")
        print(f"MAIL_PORT: {current_app.extensions['mail'].port}")
        print(f"MAIL_USE_TLS: {current_app.extensions['mail'].use_tls}")
        print(f"MAIL_USE_SSL: {current_app.extensions['mail'].use_ssl}\n")
        
        # Envío real con contexto asegurado
        msg = Message(
            'Test Final',
            recipients=['tuemail@gmail.com'],
            body='Este es el test definitivo'
        )
        mail.send(msg)
        return "¡Email enviado correctamente!"
    except Exception as e:
        current_app.logger.error(f"Fallo definitivo: {str(e)}", exc_info=True)
        return f"Error: {str(e)}", 500
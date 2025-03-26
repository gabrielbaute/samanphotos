"""Mail module for sending emails"""

from flask_mail import Mail, Message
from flask import current_app, render_template

mail = Mail()

def send_email(to, subject, template):
    """Send an email to a user
    Args:
        to (str): Email address of the recipient
        subject (str): Subject of the email
        template (str): Email template
    """
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )
    mail.send(msg)


def send_reset_email(user):
    """Send a password reset email to a user
    Args:
        user (User): User instance
    """
    token = user.get_reset_token()
    email_body = render_template("email/reset_password.html", token=token)
    send_email(user.email, "Restablecer Contraseña", email_body)

"""Extensions module. Each extension is initialized in the app factory located in app/__init__.py."""

from core.mail import Mail
from flask_login import LoginManager

mail = Mail()
login_manager = LoginManager()

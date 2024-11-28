"""Extensions module. Each extension is initialized in the app factory located in app/__init__.py."""

from flask_sqlalchemy import SQLAlchemy
from core.mail import Mail
from flask_login import LoginManager

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

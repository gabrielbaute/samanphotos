from flask_sqlalchemy import SQLAlchemy
from core.mail import Mail
from flask_login import LoginManager

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
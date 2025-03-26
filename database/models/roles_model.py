from flask_security import RoleMixin
from database.db_config import db

class Role(db.Model, RoleMixin):
    """Modelo de roles de usuario"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
"""Módulo que define los modelos de la base de datos de la aplicación."""

import uuid
from datetime import datetime

from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
)


class Role(db.Model, RoleMixin):
    """Modelo de roles de usuario"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    """Modelo de usuario"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(80), unique=False)
    password_hash = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    storage_path = db.Column(db.String(255), nullable=False)  # Ruta de almacenamiento
    active = db.Column(db.Boolean, default=True)
    confirmed_at = db.Column(db.DateTime)
    theme_preference = db.Column(db.String(10), default='light')
    fs_uniquifier = db.Column(
        db.String(64), unique=True, nullable=False, default=uuid.uuid4().hex
    )

    # Campos para el rastreo de sesiones de inicio de sesión
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer, default=0)

    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )

    @property
    def password(self):
        """Propiedad de solo lectura para la contraseña"""
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Generar el hash de la contraseña"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verificar la contraseña"""
        return check_password_hash(self.password_hash, password)


class Photo(db.Model):
    """Modelo de fotos"""

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=True, nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"))
    face_encodings = db.relationship("FaceEncoding", backref="photo", lazy="dynamic")

    # Campos de metadata
    date_taken = db.Column(db.DateTime, nullable=True)
    camera_make = db.Column(db.String(255), nullable=True)
    camera_model = db.Column(db.String(255), nullable=True)
    focal_length = db.Column(db.String(255), nullable=True)
    aperture = db.Column(db.String(255), nullable=True)
    iso = db.Column(db.String(255), nullable=True)
    gps_latitude = db.Column(db.String(255), nullable=True)
    gps_longitude = db.Column(db.String(255), nullable=True)

    user = db.relationship("User", backref=db.backref("photos", lazy="dynamic"))

class FaceEncoding(db.Model):
    """Modelo de codificaciones faciales"""

    id = db.Column(db.Integer, primary_key=True)
    encoding = db.Column(db.PickleType, nullable=False)  # Almacenar la codificación facial como binario
    name = db.Column(db.String(255), nullable=True)  # Nombre asignado al rostro
    photo_id = db.Column(db.Integer, db.ForeignKey("photo.id"), nullable=False)

class Album(db.Model):
    """Modelo de álbumes"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("albums", lazy="dynamic"))

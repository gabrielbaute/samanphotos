from database.db_config import db
from datetime import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import PickleType

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
    encoding = db.Column(MutableList.as_mutable(PickleType), nullable=False)  # Almacenar la codificación facial como binario
    name = db.Column(db.String(255), nullable=True)  # Nombre asignado al rostro
    photo_id = db.Column(db.Integer, db.ForeignKey("photo.id"), nullable=False)
    top = db.Column(db.Integer, nullable=True)
    right = db.Column(db.Integer, nullable=True)
    bottom = db.Column(db.Integer, nullable=True)
    left = db.Column(db.Integer, nullable=True)

class Album(db.Model):
    """Modelo de álbumes"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("albums", lazy="dynamic"))

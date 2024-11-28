"""Rutas para subir fotos, visualizar fotos y albums, y descargar fotos"""

import os
import uuid

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
    send_from_directory,
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.models import db, User, Photo, Album
from app.forms import UploadPhotoForm, CreateAlbumForm
from core.metadata import extract_metadata

photos = Blueprint("photos", __name__)


@photos.route("/uploads/<filename>")
def uploaded_file(filename):
    """Ruta para servir la carpeta uploads (definida por el admin)
    Args:
        filename (str): Nombre del archivo a servir
    Returns:
        file: Archivo solicitado
    """
    user_storage_path = current_user.storage_path
    return send_from_directory(user_storage_path, filename)


@photos.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Ruta para subir fotos y crear albums en el perfil del usuario."""
    upload_form = UploadPhotoForm()
    album_form = CreateAlbumForm()
    user_storage_path = current_user.storage_path
    if upload_form.validate_on_submit() and "photos" in request.files:
        files = request.files.getlist(upload_form.photos.name)
        for file in files:
            filename = secure_filename(file.filename)
            original_filename = file.filename
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(user_storage_path, unique_filename)
            file.save(filepath)
            metadata = extract_metadata(filepath)
            new_photo = Photo(
                filename=unique_filename,
                original_filename=original_filename,
                path=filepath,
                user_id=current_user.id,
                date_taken=metadata.get("date_taken"),
                camera_make=metadata.get("camera_make"),
                camera_model=metadata.get("camera_model"),
                focal_length=metadata.get("focal_length"),
                aperture=metadata.get("aperture"),
                iso=metadata.get("iso"),
                gps_latitude=metadata.get("gps_latitude"),
                gps_longitude=metadata.get("gps_longitude"),
            )
            db.session.add(new_photo)
        db.session.commit()
        flash("Fotos subidas con éxito")
        return redirect(url_for("photos.profile"))
    if album_form.validate_on_submit():
        print(f"Creating new album: {album_form.albumname.data}")
        new_album = Album(name=album_form.albumname.data, user_id=current_user.id)
        db.session.add(new_album)
        db.session.commit()  # Asegurar que el álbum se guarda en la DB y obtiene un id

        if "photos" in request.files:
            files = request.files.getlist(album_form.photos.name)
            for file in files:
                filename = secure_filename(file.filename)
                original_filename = file.filename
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                filepath = os.path.join(user_storage_path, unique_filename)
                file.save(filepath)
                metadata = extract_metadata(filepath)
                print(new_album.id)
                new_photo = Photo(
                    filename=unique_filename,
                    original_filename=original_filename,
                    path=filepath,
                    user_id=current_user.id,
                    album_id=new_album.id,  # Usar el id del álbum recién creado
                    date_taken=metadata.get("date_taken"),
                    camera_make=metadata.get("camera_make"),
                    camera_model=metadata.get("camera_model"),
                    focal_length=metadata.get("focal_length"),
                    aperture=metadata.get("aperture"),
                    iso=metadata.get("iso"),
                    gps_latitude=metadata.get("gps_latitude"),
                    gps_longitude=metadata.get("gps_longitude"),
                )
                db.session.add(new_photo)
            db.session.commit()  # Asegurar que las fotos se guardan en la DB
        else:
            db.session.commit()  # Asegurar que el álbum se guarda incluso si no hay fotos
        flash("Álbum creado con éxito!")
        return redirect(url_for("photos.profile"))
    return render_template(
        "profile.html", upload_form=upload_form, album_form=album_form
    )


@photos.route("/timeline")
@login_required
def timeline_photos():
    """Ruta para visualizar las fotos subidas por el usuario en una línea de tiempo."""
    page = request.args.get("page", 1, type=int)
    photos_db = (
        Photo.query.filter_by(user_id=current_user.id)
        .order_by(Photo.uploaded_at.desc())
        .paginate(page=page, per_page=12)
    )
    return render_template(
        "timeline.html", photos=photos_db.items, pagination=photos_db
    )


@photos.route("/photo/<int:photo_id>", methods=["GET", "POST"])
@login_required
def view_photo(photo_id):
    """Ruta para visualizar una foto en particular.
    Args:
        photo_id (int): ID de la foto a visualizar
    """
    photo = Photo.query.get_or_404(photo_id)
    if photo.user_id != current_user.id:
        flash("No tienes permiso para ver esta foto.")
        return redirect(url_for("main.timeline_photos"))
    # Método para borrar foto
    if request.method == "POST":
        db.session.delete(photo)
        db.session.commit()
        flash("Foto eliminada con éxito.")
        return redirect(url_for("photos.timeline_photos"))
    return render_template("view_photo.html", photo=photo)


@photos.route("/geolocalization", methods=["GET"])
@login_required
def geolocalization():
    """Ruta para visualizar fotos con datos de geolocalización."""
    photos_db = Photo.query.filter(
        Photo.user_id == current_user.id,
        Photo.gps_latitude.isnot(None),
        Photo.gps_longitude.isnot(None),
    ).all()
    photos_data = [
        {
            "original_filename": photo.original_filename,
            "date_taken": (
                photo.date_taken.strftime("%Y-%m-%d %H:%M:%S")
                if photo.date_taken
                else ""
            ),
            "gps_latitude": photo.gps_latitude,
            "gps_longitude": photo.gps_longitude,
        }
        for photo in photos_db
    ]
    return render_template("geolocalization.html", photos=photos_data)


@photos.route("/download_photo/<int:photo_id>", methods=["GET"])
@login_required
def download_photo(photo_id):
    """Ruta para descargar una foto.
    Args:
        photo_id (int): ID de la foto a descargar
    """
    photo = Photo.query.get_or_404(photo_id)
    if photo.user_id != current_user.id:
        flash("No tienes permiso para descargar esta foto.")
        return redirect(url_for("main.timeline_photos"))
    try:
        return send_file(
            photo.path, as_attachment=True, download_name=photo.original_filename
        )
    except Exception as e:
        flash(f"Error al descargar la foto: {e}")
        return redirect(url_for("photos.view_photo", photo_id=photo.id))


@photos.route("/albums")
@login_required
def view_albums():
    """Ruta para visualizar los albums del usuario."""
    albums = Album.query.filter_by(user_id=current_user.id).all()
    return render_template("albums.html", albums=albums)


@photos.route("/albums/<int:album_id>")
@login_required
def view_album(album_id):
    """Ruta para visualizar un album en particular.
    Args:
        album_id (int): ID del album a visualizar
    """
    album = Album.query.get_or_404(album_id)
    photos_db = Photo.query.filter_by(album_id=album_id).all()
    return render_template("album.html", album=album, photos=photos_db)

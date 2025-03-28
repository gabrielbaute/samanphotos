"""Rutas para editar y eliminar fotos, álbumes y perfil de usuario."""

import os

from flask import Blueprint, redirect, render_template, url_for, flash, request
from flask_login import login_required, current_user

from database.db_config import db
from database.models import Photo, Album
from app.forms import EditProfileForm

edits = Blueprint("edits", __name__)


@edits.route("/edit_album/<int:album_id>", methods=["GET", "POST"])
@login_required
def edit_album(album_id):
    """Editar el nombre de un álbum
    Args:
        album_id (int): ID del álbum
    """
    album = Album.query.get_or_404(album_id)
    if album.user_id != current_user.id:
        flash("No tienes permiso para realizar esta acción.")
        return redirect(url_for("photos.view_albums"))
    if request.method == "POST":
        new_name = request.form["album_name"]
        if new_name:
            album.name = new_name
            db.session.close_all()
            flash("Nombre del álbum actualizado con éxito.")
            return redirect(url_for("photos.view_albums"))
        else:
            flash("El nombre del álbum no puede estar vacío.")
    return render_template("edit/edit_album.html", album=album)


# Ruta para Editar el Perfil
@edits.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    """Editar el perfil del usuario"""
    form = EditProfileForm()
    if form.validate_on_submit():
        #current_user.first_name = form.first_name.data
        #current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        #current_user.age = form.age.data
        current_user.theme_preference = form.theme_preference.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash("Tu perfil ha sido actualizado.")
        return redirect(url_for("photos.profile"))

    #form.first_name.data = current_user.first_name
    #form.last_name.data = current_user.last_name
    form.email.data = current_user.email
    #form.age.data = current_user.age
    form.theme_preference.data = current_user.theme_preference

    # Preparar los datos de seguridad

    return render_template("edit/edit_profile.html", form=form)


@edits.route("/delete_photo/<int:photo_id>", methods=["POST"])
@login_required
def delete_photo(photo_id):
    """Eliminar una foto
    Args:
        photo_id (int): ID de la foto
    """
    photo = Photo.query.get_or_404(photo_id)
    if photo.user_id != current_user.id:
        flash("No tienes permiso para realizar esta acción.")
        return redirect(url_for("photos.timeline_photos"))
    
    if photo:
        try:
            os.remove(photo.path)
        except FileNotFoundError:
            print(f"Archivo no encontrado al intentar borrar: {photo.path}")
            flash("Error en el directorio del usuario, notificar al admin", "error")
        try:
            db.session.delete(photo)
            db.session.commit()
            flash("Foto eliminada con éxito.")
        except Exception as e:
            db.session.rollback()
            flash("Ocurrió un error al eliminar la foto.")
    else:
        flash("Foto no encontrada", "error")
    return redirect(url_for("photos.timeline_photos"))


@edits.route("/delete_album/<int:album_id>", methods=["POST"])
@login_required
def delete_album(album_id):
    """Eliminar un álbum
    Args:
        album_id (int): ID del álbum
    """
    album = Album.query.get_or_404(album_id)
    if album.user_id != current_user.id:
        flash("No tienes permiso para realizar esta acción.")
        return redirect(url_for("photos.view_albums"))
    try:
        photos = Photo.query.filter_by(album_id=album_id).all()
        for photo in photos:
            db.session.delete(photo)
        db.session.delete(album)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error al eliminar el álbum.")
    return redirect(url_for("photos.view_albums"))

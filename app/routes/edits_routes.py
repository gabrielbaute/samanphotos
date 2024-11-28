from flask import Blueprint, redirect, render_template, url_for, flash, request
from flask_login import login_required, current_user
from app.models import db, Photo, Album
from app.forms import EditProfileForm

edits = Blueprint('edits', __name__)

# Ruta para editar el nombre de un álbum
@edits.route('/edit_album/<int:album_id>', methods=['GET', 'POST'])
@login_required
def edit_album(album_id):
    album = Album.query.get_or_404(album_id)
    if album.user_id != current_user.id:
        flash('No tienes permiso para realizar esta acción.')
        return redirect(url_for('photos.view_albums'))
    if request.method == 'POST':
        new_name = request.form['album_name']
        if new_name:
            album.name = new_name
            db.session.close_all()
            flash('Nombre del álbum actualizado con éxito.')
            return redirect(url_for('photos.view_albums'))
        else:
            flash('El nombre del álbum no puede estar vacío.')
    return render_template('edit_album.html', album=album)

# Ruta para Editar el Perfil
@edits.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.age = form.age.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Tu perfil ha sido actualizado.')
        return redirect(url_for('photos.profile'))
    
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.email.data = current_user.email
    form.age.data = current_user.age
    
    # Preparar los datos de seguridad
    security_info = {
        'last_login_at': current_user.last_login_at,
        'current_login_at': current_user.current_login_at,
        'last_login_ip': current_user.last_login_ip,
        'current_login_ip': current_user.current_login_ip,
        'login_count': current_user.login_count
    }
    
    return render_template('edit_profile.html', form=form, security_info=security_info)


# Rutas para eliminar una foto
@edits.route('/delete_photo/<int:photo_id>', methods=['POST'])
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if photo.user_id != current_user.id:
        flash('No tienes permiso para realizar esta acción.')
        return redirect(url_for('photos.timeline_photos'))
    try:
        db.session.delete(photo)
        db.session.commit()
        flash('Foto eliminada con éxito.')
    except Exception as e:
        db.session.rollback()
        flash('Ocurrió un error al eliminar la foto.')
    return redirect(url_for('photos.timeline_photos'))

# Rutas para eliminar un álbum
@edits.route('/delete_album/<int:album_id>', methods=['POST'])
@login_required
def delete_album(album_id):
    album = Album.query.get_or_404(album_id)
    if album.user_id != current_user.id:
        flash('No tienes permiso para realizar esta acción.')
        return redirect(url_for('photos.view_albums'))
    try:
        photos = Photo.query.filter_by(album_id=album_id).all()
        for photo in photos:
            db.session.delete(photo)
        db.session.delete(album)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('Ocurrió un error al eliminar el álbum.')
    return redirect(url_for('photos.view_albums'))
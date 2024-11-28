import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, send_from_directory, send_file
from flask_security import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from .forms import RegisterForm, LoginForm, RestorePasswordForm, UploadPhotoForm, CreateAlbumForm, EditProfileForm
from .models import db, User, Photo, Album
from core.mail import send_reset_email
from core.metadata import extract_metadata
from core.storage import create_user_storage
import uuid

# Definir un Blueprint llamado 'main' para organizar las rutas de la aplicación
main = Blueprint('main', __name__)

# Desarrollo de rutas de la aplicación
# Ruta de Inicio
@main.route('/')
def index():
    return render_template('index.html')

# Ruta de Inicio de Sesión
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.profile'))
        else:
            flash('Usuario o contraseña inválidos')
    return render_template('login.html', form=form)

# Ruta de Registro de usuarios
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Crear el usuario y su ruta de almacenamiento
        storage_user_id = uuid.uuid4().hex
        storage_path = create_user_storage(storage_user_id)
        new_user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
            storage_path=storage_path
            )
        db.session.add(new_user)
        db.session.commit()

        # Iniciar sesión del nuevo usuario
        login_user(new_user)
        return redirect(url_for('main.profile'))
    return render_template('register.html', form=form)

# Ruta de Cierre de Sesión del usuario
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Ruta para servir la carpeta uploads (definida por el admin)
@main.route('/uploads/<filename>')
def uploaded_file(filename):
    user_storage_path = current_user.storage_path
    return send_from_directory(user_storage_path, filename)

# Ruta del Perfil del Usuaruio
@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    upload_form = UploadPhotoForm()
    album_form = CreateAlbumForm()
    user_storage_path = current_user.storage_path
    if upload_form.validate_on_submit() and 'photos' in request.files:
        files = request.files.getlist(upload_form.photos.name)
        for file in files:
            filename = secure_filename(file.filename)
            original_filename = file.filename
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(user_storage_path, unique_filename)
            file.save(filepath)
            metadata = extract_metadata(filepath)
            date_taken = metadata.get('date_taken')
            new_photo = Photo(
                filename = unique_filename,
                original_filename=original_filename,
                path = filepath,
                user_id = current_user.id,
                date_taken = metadata.get('date_taken'),
                camera_make = metadata.get('camera_make'),
                camera_model = metadata.get('camera_model'),
                focal_length = metadata.get('focal_length'),
                aperture = metadata.get('aperture'),
                iso = metadata.get('iso'),
                gps_latitude=metadata.get('gps_latitude'),
                gps_longitude=metadata.get('gps_longitude')
            )
            db.session.add(new_photo)
        db.session.commit()
        flash('Fotos subidas con éxito')
        return redirect(url_for('main.profile'))
    if album_form.validate_on_submit():
        print(f"Creating new album: {album_form.albumname.data}")
        new_album = Album(name=album_form.albumname.data, user_id=current_user.id)
        db.session.add(new_album)
        db.session.commit()  # Asegurar que el álbum se guarda en la DB y obtiene un id

        if 'photos' in request.files:
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
                    date_taken=metadata.get('date_taken'),
                    camera_make=metadata.get('camera_make'),
                    camera_model=metadata.get('camera_model'),
                    focal_length=metadata.get('focal_length'),
                    aperture=metadata.get('aperture'),
                    iso=metadata.get('iso'),
                    gps_latitude=metadata.get('gps_latitude'),
                    gps_longitude=metadata.get('gps_longitude')
                )
                db.session.add(new_photo)
            db.session.commit()  # Asegurar que las fotos se guardan en la DB
        else:
            db.session.commit()  # Asegurar que el álbum se guarda incluso si no hay fotos
        flash('Álbum creado con éxito!')
        return redirect(url_for('main.profile'))
    return render_template('profile.html', upload_form=upload_form, album_form=album_form)


# Ruta de Restablecimiento de Contraseña para el usuario
@main.route('/resset_password', methods=['GET','POST'])
def resset_password():
    form = RestorePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.')
            return redirect(url_for('main.login'))
        else:
            flash('No se encontró ninguna cuenta con ese correo electrónico.')
    return render_template('resset_password.html', form=form)

# Ruta para Visualizar Álbumes
@main.route('/albums')
@login_required
def view_albums():
    albums = Album.query.filter_by(user_id=current_user.id).all()
    return render_template('albums.html', albums=albums)

# Ruta para Visualizar un Album concreto
@main.route('/albums/<int:album_id>')
@login_required
def view_album(album_id):
    album = Album.query.get_or_404(album_id)
    photos = Photo.query.filter_by(album_id=album_id).all()
    return render_template('album.html', album=album, photos=photos)

# Ruta para Visualizar Fotos en Línea de Tiempo
@main.route('/timeline')
@login_required
def timeline_photos():
    page = request.args.get('page', 1, type=int)
    photos = Photo.query.filter_by(user_id=current_user.id).order_by(Photo.uploaded_at.desc()).paginate(page=page, per_page=12)
    return render_template('timeline.html', photos=photos.items, pagination=photos)

# Ruta para mostrar una foto
@main.route('/photo/<int:photo_id>', methods=['GET', 'POST'])
@login_required
def view_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if photo.user_id != current_user.id:
        flash('No tienes permiso para ver esta foto.')
        return redirect(url_for('main.timeline_photos'))
    # Método para borrar foto
    if request.method == 'POST':
        db.session.delete(photo)
        db.session.commit()
        flash('Foto eliminada con éxito.')
        return redirect(url_for('main.timeline_photos'))
    return render_template('view_photo.html', photo=photo)

# Ruta de descargas
@main.route('/download_photo/<int:photo_id>', methods=['GET'])
@login_required
def download_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if photo.user_id != current_user.id:
        flash('No tienes permiso para descargar esta foto.')
        return redirect(url_for('main.timeline_photos'))
    try:
        return send_file(photo.path, as_attachment=True, download_name=photo.original_filename)
    except Exception as e:
        flash(f'Error al descargar la foto: {e}')
        return redirect(url_for('main.view_photo', photo_id=photo.id))

# Ruta de geolocalización
@main.route('/geolocalization', methods=['GET'])
@login_required
def geolocalization():
    photos = Photo.query.filter(Photo.user_id == current_user.id, Photo.gps_latitude.isnot(None), Photo.gps_longitude.isnot(None)).all()
    photos_data = [
        {
            "original_filename": photo.original_filename,
            "date_taken": photo.date_taken.strftime('%Y-%m-%d %H:%M:%S') if photo.date_taken else '',
            "gps_latitude": photo.gps_latitude,
            "gps_longitude": photo.gps_longitude
        }
        for photo in photos
    ]
    return render_template('geolocalization.html', photos=photos_data)

# Rutas para eliminar una foto
@main.route('/delete_photo/<int:photo_id>', methods=['POST'])
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if photo.user_id != current_user.id:
        flash('No tienes permiso para realizar esta acción.')
        return redirect(url_for('main.timeline_photos'))
    try:
        db.session.delete(photo)
        db.session.commit()
        flash('Foto eliminada con éxito.')
    except Exception as e:
        db.session.rollback()
        flash('Ocurrió un error al eliminar la foto.')
    return redirect(url_for('main.timeline_photos'))

# Rutas para eliminar un álbum
@main.route('/delete_album/<int:album_id>', methods=['POST'])
@login_required
def delete_album(album_id):
    album = Album.query.get_or_404(album_id)
    if album.user_id != current_user.id:
        flash('No tienes permiso para realizar esta acción.')
        return redirect(url_for('main.view_albums'))
    try:
        photos = Photo.query.filter_by(album_id=album_id).all()
        for photo in photos:
            db.session.delete(photo)
        db.session.delete(album)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('Ocurrió un error al eliminar el álbum.')
    return redirect(url_for('main.view_albums'))

# Ruta para editar el nombre de un álbum
@main.route('/edit_album/<int:album_id>', methods=['GET', 'POST'])
@login_required
def edit_album(album_id):
    album = Album.query.get_or_404(album_id)
    if album.user_id != current_user.id:
        flash('No tienes permiso para realizar esta acción.')
        return redirect(url_for('main.view_albums'))
    if request.method == 'POST':
        new_name = request.form['album_name']
        if new_name:
            album.name = new_name
            db.session.close_all()
            flash('Nombre del álbum actualizado con éxito.')
            return redirect(url_for('main.view_albums'))
        else:
            flash('El nombre del álbum no puede estar vacío.')
    return render_template('edit_album.html', album=album)

# Ruta para Editar el Perfil
@main.route('/edit_profile', methods=['GET', 'POST'])
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
        return redirect(url_for('main.profile'))
    
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
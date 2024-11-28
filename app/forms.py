from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Optional

class RegisterForm(FlaskForm):
    email = EmailField('Correo Electrónico', validators=[DataRequired(), Email()])
    username = StringField('Nombnre', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    email = EmailField('Correo Electrónico', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class RestorePasswordForm(FlaskForm):
    email = EmailField('Correo Electrónico', validators=[DataRequired()])
    submit = SubmitField('Recuperar Contraseña')

class CreateAlbumForm(FlaskForm):
    albumname = StringField('Nombre del album', validators=[DataRequired()])
    photos = FileField('Agregar Fotos', render_kw={"multiple": True})
    submit = SubmitField('Crear album')

class UploadPhotoForm(FlaskForm):
    photos = FileField('Subir Foto', validators=[DataRequired(), FileRequired()], render_kw={"multiple": True})
    submit = SubmitField('Subir')

class EditProfileForm(FlaskForm):
    first_name = StringField('Nombre', validators=[Optional()])
    last_name = StringField('Apellido', validators=[Optional()])
    email = StringField('Correo', validators=[DataRequired(), Email()])
    age = IntegerField('Edad', validators=[Optional()])
    password = PasswordField('Nueva Contraseña', validators=[Optional()])
    password2 = PasswordField('Repetir Nueva Contraseña', validators=[EqualTo('password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Actualizar Perfil')
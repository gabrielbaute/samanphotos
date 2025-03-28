from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class CreateAlbumForm(FlaskForm):
    """Formulario para crear un nuevo album."""

    albumname = StringField("Nombre del album", validators=[DataRequired()])
    #photos = FileField("Agregar Fotos", render_kw={"multiple": True})
    submit = SubmitField("Crear album")


class UploadPhotoForm(FlaskForm):
    """Formulario para subir fotos a un album."""

    photos = FileField(
        "Subir Foto",
        validators=[DataRequired(), FileRequired()],
        render_kw={"multiple": True},
    )
    album = SelectField("Album", coerce=int, choices=[])
    submit = SubmitField("Subir")
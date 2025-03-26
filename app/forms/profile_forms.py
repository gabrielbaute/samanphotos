from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Optional

class EditProfileForm(FlaskForm):
    """Formulario para editar el perfil del usuario."""

    first_name = StringField("Nombre", validators=[Optional()])
    last_name = StringField("Apellido", validators=[Optional()])
    email = StringField("Correo", validators=[DataRequired(), Email()])
    age = IntegerField("Edad", validators=[Optional()])
    password = PasswordField("Nueva Contraseña", validators=[Optional()])
    password2 = PasswordField(
        "Repetir Nueva Contraseña",
        validators=[EqualTo("password", message="Las contraseñas deben coincidir")],
    )
    theme_preference = SelectField(
        "Tema",
        choices=[("light", "Claro"), ("dark", "Oscuro")]
    )
    submit = SubmitField("Actualizar Perfil")

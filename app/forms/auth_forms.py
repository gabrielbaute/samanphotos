from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

class LoginForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repita su contraseña')
    submit = SubmitField('Crear cuenta')

class ResendConfirmationForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Reenviar correo de confirmación')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Reenvíar link')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nueva contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar nueva contraseña', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Reestablecer contraseña')

class ReactivateAccountForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Reactivar cuenta')

class TOTPForm(FlaskForm):
    totp_code = StringField('Código del autenticador', validators=[DataRequired()])
    submit = SubmitField('Verificar')

class VerificationCodeForm(FlaskForm):
    code = StringField('Código de verificación', validators=[
        DataRequired(),
        Length(min=6, max=6),
        Regexp(r'^\d{6}$', message="El código debe ser un número de 6 dígitos.")
    ])
    submit = SubmitField('Verificar código')
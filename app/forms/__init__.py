from .auth_forms import(
    LoginForm,
    RegisterForm,
    ResendConfirmationForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    TOTPForm,
    ReactivateAccountForm,
    VerificationCodeForm
    )
from .photos_forms import(
    CreateAlbumForm,
    UploadPhotoForm
)

__all__ = [
    'LoginForm',
    'RegisterForm',
    'ResendConfirmationForm',
    'ForgotPasswordForm',
    'ResetPasswordForm',
    'TOTPForm',
    'ReactivateAccountForm',
    'VerificationCodeForm',
    'CreateAlbumForm',
    'UploadPhotoForm'
]
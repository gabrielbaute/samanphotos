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
from .profile_forms import EditProfileForm

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
    'UploadPhotoForm',
    'EditProfileForm'
]
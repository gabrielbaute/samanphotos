"""Genera claves secretas para la aplicación Flask y Flask-Security."""
import secrets

def generate_secret_key():
    """Genera una clave secreta para la aplicación Flask 32 caracteres."""
    return secrets.token_hex(32)

def generate_salt():
    """Genera una clave secreta para Flask-Security 16 caracteres."""
    return secrets.token_hex(16)

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print(f"Your secret key is: {secret_key}")
    print("Please add the following line to your .env file:")
    print(f"SECRET_KEY={secret_key}")

    secret_key = generate_salt()
    print(f"Your secret key is: {secret_key}")
    print("Please add the following line to your .env file:")
    print(f"SECURITY_PASSWORD_SALT={secret_key}")

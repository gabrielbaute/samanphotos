import os
import secrets

def generate_secret_key():
    return secrets.token_hex(32)  # Genera una clave secreta de 64 caracteres

def generate_salt():
    return secrets.token_hex(16)  # Genera una clave secreta de 64 caracteres

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print(f"Your secret key is: {secret_key}")
    print("Please add the following line to your .env file:")
    print(f"SECRET_KEY={secret_key}")

    secret_key = generate_salt()
    print(f"Your secret key is: {secret_key}")
    print("Please add the following line to your .env file:")
    print(f"SECURITY_PASSWORD_SALT={secret_key}")
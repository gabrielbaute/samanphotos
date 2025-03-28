"""Extensions module. Each extension is initialized in the app factory located in app/__init__.py."""
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_caching import Cache


login_manager = LoginManager()
cache=Cache()
jwt=JWTManager()
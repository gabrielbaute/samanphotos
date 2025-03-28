"""Register all blueprints in the app."""

from .auth_routes import auth
from .edits_routes import edits
from .photo_routes import photos
from .public_routes import public


def register_blueprints(app):
    """Register all blueprints in the app."""
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(edits, url_prefix="/edit")
    app.register_blueprint(photos, url_prefix="/photos")
    app.register_blueprint(public)

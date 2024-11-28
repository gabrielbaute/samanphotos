from .auth_routes import auth
from .edits_routes import edits
from .photo_routes import photos
from .public_routes import public

def register_blueprints(app):
    app.register_blueprint(auth)
    app.register_blueprint(edits)
    app.register_blueprint(photos)
    app.register_blueprint(public)
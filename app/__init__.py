import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin
from flask_migrate import Migrate
from flask_restful import Api
from flask_caching import Cache
from flask_login import LoginManager
from .extensions import db, mail, login_manager
from .models import User, Role
from core.storage import create_user_storage
import uuid

cache = Cache()

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object('config.Config')
    
    with app.app_context():
        db.init_app(app)
        mail.init_app(app)
        migrate = Migrate(app, db)
        admin = Admin(app)
        cache.init_app(app)
        login_manager.init_app(app)

        login_manager.login_view = 'main.login'

        # Registrar rutas personalizadas
        from app.routes import register_blueprints
        register_blueprints(app)

        # Inicializar Flask-Security después de registrar rutas personalizadas
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security = Security()
        security.init_app(app, datastore=user_datastore, register_blueprint=False)

        db.create_all()
        create_admin_user()
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_admin_user():
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')

    if not User.query.filter_by(email=admin_email).first():
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)
            db.session.commit()
        
        # Crear la ruta de almacenamiento antes de crear el usuario
        storage_user_id = uuid.uuid4().hex # Generar un ID temporal único para crear la ruta
        storage_path = create_user_storage(storage_user_id)

        admin_user = User(
                    email=admin_email,
                    password=admin_password,
                    roles=[admin_role],
                    storage_path=storage_path
                        )
        db.session.add(admin_user)
        db.session.commit()
from flask_mail import Mail
from config import Config

appname = Config.APP_NAME.upper()
mail = Mail()
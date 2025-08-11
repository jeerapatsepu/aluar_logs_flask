from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from uuid import uuid4

db = SQLAlchemy()
bcrypt = Bcrypt()
uid = uuid4()
login_manager = LoginManager()
login_manager.login_message = u"Require login"
login_manager.login_message_category = "info"
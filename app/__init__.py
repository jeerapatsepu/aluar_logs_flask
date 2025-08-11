import os
import secrets
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_smorest import Api
from datetime import timedelta
from dotenv import load_dotenv
from app.jwt import handle_jwt
from app.extension import db, bcrypt, login_manager
import models
from resources.auth.auth_create.auth_create import blp as AuthCreateBlueprint
from resources.auth.auth_login import blp as AuthLoginBlueprint
from resources.log.log_create import blp as LogCreateBlueprint
from resources.log.log_list import blp as LogListBlueprint

def create_app(db_url=None) -> Flask:
    load_dotenv()
    app = Flask(__name__)

    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_VERSION"] = "v1"
    app.config["API_TITLE"] = "Log API"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)
    handle_jwt(app)
    api = Api(app)
    api.register_blueprint(AuthCreateBlueprint)
    api.register_blueprint(AuthLoginBlueprint)
    api.register_blueprint(LogCreateBlueprint)
    api.register_blueprint(LogListBlueprint)

    return app
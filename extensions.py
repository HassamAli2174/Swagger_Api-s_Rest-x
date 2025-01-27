from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
api = Api()
migrate = Migrate()
jwt = JWTManager()

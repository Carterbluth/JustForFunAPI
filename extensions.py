from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_login import LoginManager

db = SQLAlchemy(session_options={"expire_on_commit": False})
ma = Marshmallow()
jwt = JWTManager()
login_manager = LoginManager()

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from config import const as CONSTANTS
from services import database_service
from extensions import db, ma, jwt, login_manager
from api.v1.users import users
from api.v1.drama import drama
from api.v1.authentication import authentication

application = Flask(__name__)
api = Api(application)

def create_app():
    print("create_app. Preparing to setup Flask")
    api_v1_cors_config = {
        "methods": ["OPTIONS", "GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Authorization", "Content-Type"]
    }
    CORS(application, resources={"/api/v1/*": api_v1_cors_config})
    configure_app(application)
    register_extensions(application)
    return application


def register_extensions(application):
    print("Registering extensions")
    db.init_app(application)
    print("db init passed")
    ma.init_app(application)
    print("ma init passed")
    login_manager.init_app(application)

    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        try:
            return User.query.filter(User.id == user_id).first()
        finally:
            return None

def configure_app(application):
    print("Configuring app")
    application.config['SQLALCHEMY_DATABASE_URI'] = CONSTANTS.DB_CONNECTION_STRING
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config['JWT_BLACKLIST_ENABLED'] = True
    application.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['refresh']

def register_blueprints(application):
    application.register_blueprint(authentication, url_prefix='/api/v1/auth')
    application.register_blueprint(users, url_prefix='/api/v1/users')







print("Preparing to call create_app")
app = create_app()
register_blueprints(app)
database_service.init_session()

if __name__ == '__main__':
    app.run(debug=True)


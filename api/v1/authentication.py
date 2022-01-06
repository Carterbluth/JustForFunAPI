import sqlalchemy
from extensions import db
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.user import User, UserSchema
from services.flask_helper_service import validate_request
from services.crypt_service import pwd_context
from services.error_service import build_error_response, parse_sql_alchemy_errors, ErrorTopics
import logging


log = logging.getLogger()
authentication = Blueprint('auth', __name__)




# Login route used for validating a user's credentials and returning their user details and auth tokens
@authentication.route("/login", methods=["POST"])
@validate_request(
    enforce_json=True,
    required_fields=['username', 'password'],
    enforced_types=[('username', str), ('password', str)])
def login():
    log.info("authentication.login")
    user_schema = UserSchema()
    # Get the email and password from the request body
    body = request.get_json()
    username = body.get('username')
    password = body.get('password')
    # Validate the supplied credentials
    db_user = User.query.filter(User.username == username).first()

    # No user record found in the database
    if db_user is None:
        error = build_error_response(ErrorTopics.AUTH, "Invalid username or password", sub_topic="invalid_credentials")
        return jsonify(error), 401

    # Verify the provided password with the hashed value
    valid_password = pwd_context.verify(password, db_user.password)

    if not valid_password:
        error = build_error_response(ErrorTopics.AUTH, "Invalid email or password", sub_topic="invalid_credentials")
        return jsonify(error), 401

    # Attempt to log the user in using their credentials for the specified organization
    user = user_schema.dump(db_user)

    # Create tokens for the newly created user
    # tokens = token_service.generate_user_tokens(user["id"], fresh_token=True)

    response = {
        'user': user,
    }
    return jsonify(response), 200

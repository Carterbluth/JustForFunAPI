from flask import Blueprint, request, jsonify
from models.user import User, UserSchema
import hashlib

from services.error_service import build_error_response, ErrorTopics

users = Blueprint('users', __name__)


# Route to get a list of users
@users.route('', methods=['get'])
def get_users():
    users_schema = UserSchema(many=True)

    users = User.query.all()

    # Get users
    users_data = users_schema.dump(users)

    return jsonify(users_data), 200



# Route for creating a new users record
@users.route("", methods=['POST'])
def create_user():
    users_schema = UserSchema()

    body = request.get_json(force=True)
    user = users_schema.load(body['user'])
    exist_user = User.query.filter(User.username == user.username).first()
    if exist_user is not None:
        error = build_error_response(ErrorTopics.DATA, "Username already exists", sub_topic="invalid_username")
        return jsonify(error), 401
    user.password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()
    user.update()

    user = users_schema.dump(user)
    response = {
        'users': user
    }
    return jsonify(response), 201


# Route for updating a users record
@users.route("/<id>", methods=['POST'])
def update_user(id):
    users_schema = UserSchema()
    body = request.get_json(force=True)

    user = User.query.get(id)
    user.update(body['user'])

    user = users_schema.dump(users)
    response = {
        'user': user
    }
    return jsonify(response), 200


# Route used for deleting a users record
@users.route("/<id>", methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    user.delete()

    return '', 204

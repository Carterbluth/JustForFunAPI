from flask import Blueprint, request, jsonify
from models.drama import Drama
drama = Blueprint('auth', __name__)



# Route for creating a new users record
@drama.route("", methods=['POST'])
def create_drama():
    drama_schema = Drama()

    body = request.get_json(force=True)
    drama_data = drama_schema.load(body['drama'])
    drama_data.update()

    drama = drama_schema.dump(drama_data)
    response = {
        'drama': drama
    }
    return jsonify(response), 201

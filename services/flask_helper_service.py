from functools import wraps
from flask import request, jsonify
from services.error_service import Error, ErrorTopics, build_error_response
import logging

log = logging.getLogger()


# This function is used to help validate incoming requests
def validate_request(enforce_json=False, required_fields=None, required_params=None, enforced_types=None):
    if enforced_types is None:
        enforced_types = []
    if required_params is None:
        required_params = []
    if required_fields is None:
        required_fields = []

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            log.info('services.flask_helpers_service')
            errors = []

            # If enforce_json, verify that valid json was passed in
            if enforce_json and not request.is_json:
                error = build_error_response(ErrorTopics.REQUEST_ERROR, "Missing JSON request body")
                return jsonify(error), 400

            for param in required_params:
                param_data = request.args.get(param, None)
                if param_data is None:
                    errors.append(
                        Error(
                            ErrorTopics.REQUEST_ERROR,
                            "%s parameter is required" % param,
                            sub_topic=param
                        ).toJSON()
                    )

            for field in required_fields:
                field_data = request.get_json().get(field, None)
                if field_data is None:
                    errors.append(
                        Error(
                            ErrorTopics.REQUEST_ERROR,
                            "%s field is required" % field,
                            sub_topic=field
                        ).toJSON()
                    )

            for field_type in enforced_types:
                field_name = field_type[0]
                required_type = field_type[1]

                field_value = request.json.get(field_name, None) or request.args.get(field_name, None)
                if field_value is not None:
                    if not isinstance(field_value, required_type):
                        errors.append(
                            Error(
                                ErrorTopics.REQUEST_ERROR,
                                "%s should be of type %s" % (field_name, required_type.__name__),
                                sub_topic=field_name
                            ).toJSON()
                        )

            # Return any errors
            if len(errors) > 0:
                return jsonify({"errors": errors}), 400

            return f(*args, **kwargs)
        return wrapped
    return decorator

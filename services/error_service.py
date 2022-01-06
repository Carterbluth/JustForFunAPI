from enum import Enum


class ErrorTopics(Enum):
    ERROR = "error",
    AUTH = "auth",
    UNAUTHORIZED = "unauthorized",
    REQUEST_ERROR = "request_error",
    MISSING_PARAMETER = "missing_parameter",
    MISSING_FIELD = "missing_field",
    DATA = "data",
    USER = "user"


class Error():
    topic = "",
    sub_topic = "",
    message = ""

    def __init__(self, topic, message, sub_topic=None):
        self.topic = topic.value[0]
        self.sub_topic = sub_topic
        self.message = message

    def toJSON(self):
        return {
            "topic": self.topic,
            "message": self.message,
            "sub_topic": self.sub_topic
        }


def build_error_response(topic, message, sub_topic=None):
    errors = [
        Error(topic, message, sub_topic).toJSON()
    ]
    return {"errors": errors}


def parse_sql_alchemy_errors(alchemy_errors):
    errors = []

    # Loop through all sql alchemy error keys
    for key, value in alchemy_errors.items():
        for error in value:
            errors.append(
                Error(ErrorTopics.REQUEST_ERROR, error).toJSON()
            )

    return {"errors": errors}

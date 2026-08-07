from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        message = getattr(exc, "default_detail", "Request failed")

        response.data = {
            "success": False,
            "message": str(message),
            "errors": response.data,
            "status_code": response.status_code,
        }

    return response

class EmailRequired(APIException):
    status_code = 400
    default_detail = "Email is required."
    default_code = "EMAIL_REQUIRED"


class InvalidEmailFormat(APIException):
    status_code = 400
    default_detail = "Invalid email format."
    default_code = "INVALID_EMAIL_FORMAT"

class InvalidPassword(APIException):
    status_code = 400
    default_detail = "Password validation failed."
    default_code = "INVALID_PASSWORD"

class EmailAlreadyExists(APIException):
    status_code = 409
    default_detail = "An account with this email already exists."
    default_code = "EMAIL_ALREADY_EXISTS"


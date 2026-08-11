from rest_framework.exceptions import APIException
from rest_framework import status


class InvalidChoice(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid choice."
    default_code = "INVALID_CHOICE"
from rest_framework.exceptions import APIException
from rest_framework import status


class InvalidParticipantCount(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ("A group conversation must have at least two participants.")
    default_code = "INVALID_PARTICIPANT_COUNT"

class DuplicateParticipant(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Participant IDs must be unique."
    default_code = "DUPLICATE_PARTICIPANT"

class InvalidGroupName(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Group name is required and must be at least 3 characters long."
    default_code = "INVALID_GROUP_NAME"

class InvalidParticipant(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "One or more participants are invalid."
    default_code = "INVALID_PARTICIPANT"

class CannotAddSelf(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You cannot add yourself to the conversation."
    default_code = "CANNOT_ADD_SELF"

class InvalidParticipant(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "INVALID_PARTICIPANT"
    default_detail = "One or more participants are invalid or inactive."
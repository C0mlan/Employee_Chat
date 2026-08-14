from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from authcore.repositories import (EmployeeRepository)

from common.apiexceptions.authcore import (
    EmailRequired,
    InvalidEmailFormat,
    EmailAlreadyExists,
    InvalidCredentials
)


class EmailValidator:

    @staticmethod
    def validate_email(email: str) -> str:
        if email is None:
            raise EmailRequired(
                detail={"email": "Email cannot be null"}
            )
        if not email:
            raise EmailRequired(
                detail={
                    "email": "Email is required"
                }
            )
        
        email = email.strip().lower()

        try:
            validate_email(email)
        except ValidationError:
            raise InvalidEmailFormat(
                detail={"email": "Invalid email format"}
            )
        return email

    @staticmethod
    def validate_email_uniqueness(email):

        if EmployeeRepository.exists_by_email(email):

            raise EmailAlreadyExists(
                detail={
                    "email":
                    "employee with this email already exists."
                }
            )

    @staticmethod
    def validate_login_email(email):
        '''this will return exception when '''
        if not email:
            raise InvalidCredentials()
        return email

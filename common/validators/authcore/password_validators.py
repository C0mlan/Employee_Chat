import re

from django.conf import settings

from common.apiexceptions.authcore import InvalidPassword

MIN_PASSWORD_LENGTH = 8
class PasswordValidator:

    @staticmethod
    def validate_password_strength(password: str):
        minimum_length = MIN_PASSWORD_LENGTH

        if len(password) < minimum_length:
            raise InvalidPassword(
                detail={
                    "password":
                    f"Password must be at least {minimum_length} characters"
                }
            )

        if not re.search(r"[A-Z]", password):
            raise InvalidPassword(
                detail={
                    "password": "Password must contain uppercase letter"
                }
            )

        if not re.search(r"[a-z]", password):
            raise InvalidPassword(
                detail={
                    "password": "Password must contain lowercase letter"
                }
            )

        if not re.search(r"[0-9]", password):
            raise InvalidPassword(
                detail={
                    "password": "Password must contain a number"
                }
            )

        if not re.search(r"[\W_]", password):
            raise InvalidPassword(
                detail={
                    "password": "Password must contain special character, "
                }
            )

    @staticmethod
    def validate_passwords_match(password: str, confirm_password:str) -> None:
        """
        Ensures the password and confirmation password are identical.
        """
        if password != confirm_password:
            raise InvalidPassword(
                detail={
                    "confirm_password": "Passwords do not match."
                }
            )
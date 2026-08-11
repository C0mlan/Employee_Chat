
import pytest
from common.validators.authcore.password_validators import PasswordValidator

from common.apiexceptions.authcore import InvalidPassword

@pytest.mark.unit
class TestValidatePasswordStrength:

    def test_rejects_short_password(self):
        with pytest.raises(InvalidPassword) as exc:
            PasswordValidator.validate_password_strength("Pass1!")

        assert exc.value.detail == {
            "password": "Password must be at least 8 characters"
        }
    def test_requires_uppercase_letter(self):
        with pytest.raises(InvalidPassword) as exc:
            PasswordValidator.validate_password_strength("password123!")

        assert exc.value.detail == {
            "password": "Password must contain uppercase letter"
        }
    def test_requires_lowercase_letter(self):
        with pytest.raises(InvalidPassword) as exc:
            PasswordValidator.validate_password_strength("PASSWORD123!")

        assert exc.value.detail == {
            "password": "Password must contain lowercase letter"
        }
    def test_requires_special_character(self):
        with pytest.raises(InvalidPassword) as exc:
            PasswordValidator.validate_password_strength("Password123")

        assert exc.value.detail == {
            "password": "Password must contain special character, "
        }

    def test_passwords_do_not_match(self):
        with pytest.raises(InvalidPassword) as exc:
            PasswordValidator.validate_passwords_match(
                "Password123!",
                "Password456!"
            )

        assert exc.value.detail == {
            "confirm_password": "Passwords do not match."
        }
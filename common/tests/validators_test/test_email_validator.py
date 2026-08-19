
import pytest
from unittest.mock import patch

from common.validators.authcore.email_validator import EmailValidator
from common.apiexceptions.authcore import (
    EmailRequired,
    InvalidEmailFormat,
    EmailAlreadyExists
)
@pytest.mark.unit
class TestValidateEmail:

    def test_returns_normalized_email(self):
        email = EmailValidator.validate_email("  TEST@Example.COM ")
        assert email == "test@example.com"

    def test_raises_when_email_is_none(self):
        with pytest.raises(EmailRequired):
            EmailValidator.validate_email(None)

    def test_raises_when_email_is_empty(self):
        with pytest.raises(EmailRequired):
            EmailValidator.validate_email("")

    def test_invalid_email(self):
        with pytest.raises(InvalidEmailFormat):
            EmailValidator.validate_email("invalid-email")


    @patch("apps.authcore.repositories.EmployeeRepository.exists_by_email")
    def test_existing_email_raises_exception(self, mock_exists):
        mock_exists.return_value = True

        with pytest.raises(EmailAlreadyExists):
            EmailValidator.validate_email_uniqueness(
                "test@example.com"
            )

    @patch("apps.authcore.repositories.EmployeeRepository.exists_by_email")
    def test_new_email_passes(self, mock_exists):
        mock_exists.return_value = False

        EmailValidator.validate_email_uniqueness(
            "test@example.com"
        )
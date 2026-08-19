import pytest
from common.constants.routes import RouteNames
from authcore.services.auth_services import AuthService
from rest_framework_simplejwt.tokens import AccessToken

@pytest.mark.unit
class TestLoginEmployeeunit:
    def test_generate_tokens(self, regular_user):
        tokens = AuthService._generate_tokens(regular_user)

        access = AccessToken(tokens["access"])

        assert access["user_id"] == str(regular_user.id)
        assert access["role"] == regular_user.role
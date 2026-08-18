import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from common.constants.routes import RouteNames

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.integration
class TestLoginEmployeeIntegration: 
        
    def test_employee_can_register(self, api_client, regular_user):
            login_url = reverse(RouteNames.AuthCore.LOGIN)

            payload = {
            "email": regular_user.email,
            "password": "StrongPassword123!",
            }

            response = api_client.post(
                login_url,
                payload,
                format="json",
            )

            assert response.status_code == 200
            assert response.data["success"] is True
            assert response.data["response_code"] == "LOGIN_SUCCESS"
            assert "access" in response.data["data"]
            assert "refresh" in response.data["data"]

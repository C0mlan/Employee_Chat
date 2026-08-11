import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from common.constants.routes import RouteNames

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.integration
class TestRegisterEmployeeIntegration: 

    def test_employee_can_register(self, api_client):
        register_url = reverse(RouteNames.AuthCore.REGISTER)

        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!",
        }

        response = api_client.post(register_url, payload, format="json")

        assert response.status_code == 201
        assert response.data["response_code"] == "USER_CREATED"
        assert response.data["message"] == "Employee registered successfully."
        assert "emp_id" in response.data["data"]



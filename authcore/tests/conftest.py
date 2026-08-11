import pytest
from rest_framework.test import APIClient
# from apps.accounts.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        email="admin@test.com",
        password="Admin123!",
        full_name="Admin User",
        role="SUPER_ADMIN",
    )


@pytest.fixture
def authenticated_admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        email="regular@example.com",
        password="password123",
        full_name="Regular User",
        
    )
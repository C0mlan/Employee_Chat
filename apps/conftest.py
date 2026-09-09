import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from common.constants.roles import Roles
from apps.messaging.models import Conversation, ConversationParticipant
import secrets

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        email="admin@test.com",
        password="AdminPassword123!",
        role=Roles.ADMIN,
    )


@pytest.fixture
def authenticated_admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def user_factory(db):
    def make_user(**kwargs):
        defaults = {"email": f"user_{secrets.token_hex(4)}@example.com",
            "password": "StrongPassword123!",
            "role": Roles.EMPLOYEE,
            "emp_id": secrets.token_hex(4),
            
        }
        defaults.update(kwargs)

        return User.objects.create_user(**defaults)

    return make_user

@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        first_name="john",
        last_name ="doe",
        email="john@example.com",
        password="StrongPassword123!",
        role= Roles.EMPLOYEE,  
    )


@pytest.fixture
def conversation_factory(db):
    def create_conversation(**kwargs):
        defaults = {
            "conversation_type": "GROUP",
            "group_name": "Test Group",
        }
        defaults.update(kwargs)

        return Conversation.objects.create(**defaults)

    return create_conversation

@pytest.fixture
def conversation_participant_factory(db, user_factory, conversation_factory):
    def create_conversation_participant(**kwargs):
        defaults = {
            "conversation": conversation_factory(),
            "user": user_factory(),
        }
        defaults.update(kwargs)

        return ConversationParticipant.objects.create(**defaults)

    return create_conversation_participant

@pytest.fixture
def websocket_test_data(
    user_factory,
    conversation_factory,
    conversation_participant_factory,
):
    user = user_factory(
        first_name="John",
        last_name="Doe",
    )

    conversation = conversation_factory(
        conversation_type="GROUP",
        group_name="Backend Engineers",
    )

    conversation_participant_factory(
        conversation=conversation,
        user=user,
    )

    return user, conversation

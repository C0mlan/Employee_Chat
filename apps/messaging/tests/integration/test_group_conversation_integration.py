import pytest
import secrets
from apps.messaging.models import Conversation
from django.urls import reverse
from apps.messaging.views import CreateConversationAPI
from common.constants.routes import RouteNames
from apps.messaging.repositories.conversation_repositories import ConversationRepository
from apps.messaging.models import Conversation, ConversationParticipant
from common.constants.conversation_type import Type

@pytest.mark.django_db
@pytest.mark.integration
class TestGroupConversationIntegration:
    
    def test_create_group_conversation_api_success(api_client, authenticated_admin_client,create_user):
        create_group_conversation = reverse(RouteNames.Messaging.CREATEGROUPCONVERSATION)
        user1 = create_user(
            email="another@user1.com",
            password= "StrongPassword123",
            emp_id=secrets.token_hex(4),

        )
        user2 = create_user(
            email="another@user2.com",
            password= "StrongPassword123",
            emp_id=secrets.token_hex(4),
        )

        data = {
            "participant_ids": [
                str(user1.id),
                str(user2.id),
            ],
            "group_name": "Engineering Team",
        }

        response = authenticated_admin_client.post(
            create_group_conversation,
            data,
            format="json",
        )
        
        assert response.status_code == 201
        assert response.data["success"] is True
        assert response.data["data"]["group_name"] == "Engineering Team"
        assert response.data["data"]["type"] == "GROUP"
        assert response.data["data"]["participant_count"] == 2

    def test_create_group_conversation(self, regular_user, create_user):
        participant_1 =create_user(
            email="employee1@example.com",
            password="Password123!",
            emp_id=secrets.token_hex(4),
            )

        participant_2 = create_user(
            email="employee2@example.com",
            password="Password123!",
             emp_id=secrets.token_hex(4),)

        participants = [
            regular_user,
            participant_1,
            participant_2,
        ]

        conversation = ConversationRepository.create_conversation(
            conversation_type=Type.GROUP,
            group_name="Engineering Team",
            description="Engineering discussion",
            creator=regular_user,
            participants=participants,
        )

        assert conversation.conversation_type == Type.GROUP
        assert conversation.group_name == "Engineering Team"
        assert conversation.created_by == regular_user

        assert ConversationParticipant.objects.filter(conversation=conversation).count() == 3
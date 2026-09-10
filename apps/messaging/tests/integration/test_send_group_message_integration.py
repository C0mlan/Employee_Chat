import pytest
from unittest.mock import Mock, patch
from apps.messaging.models import Conversation, Message
from common.constants.routes import RouteNames
from django.urls import reverse
from rest_framework import status
import uuid
from apps.messaging.repositories.message_repositories import MessageRepository

@pytest.mark.django_db
@pytest.mark.integration
class TestSendGroupMessageIntegration:
    @patch(
        "apps.messaging.services.message_services."
        "MessageService._send_message_to_conversation"
    )
    def test_send_group_message_authenticated_success(
        self,
        mock_send_message_to_conversation,
        api_client,
        user_factory,
        conversation_factory,
        conversation_participant_factory,
        django_capture_on_commit_callbacks
        ):
        url = reverse(RouteNames.Messaging.SENDGROUPMESSAGE)

        sender = user_factory(
            first_name="John",
            last_name="Doe",
        )

        conversation = conversation_factory(
            conversation_type="GROUP",
            group_name="Backend Engineers",
        )

        conversation_participant_factory(
            conversation=conversation,
            user=sender,
        )

        api_client.force_authenticate(user=sender)

        request_payload = {
            "message_type": "message.send",
            "conversation_id": str(conversation.id),
            "content": "Hello, team!",
            "idempotency_key": "c97c9e8c-3f28-4f5f-8daf-7b3cb2783f5c",
        }

        with django_capture_on_commit_callbacks(execute=True) as callbacks:
            response = api_client.post(
                url,
                data=request_payload,
                format="json",
            )
        assert response.status_code == status.HTTP_200_OK
        assert len(callbacks) == 1

        message = Message.objects.get(
            conversation_id=conversation.id,
            sender_id=sender.id,
            content="Hello, team!",
        )

        conversation.refresh_from_db()

        assert conversation.last_message_id == message.id
        assert conversation.last_message_at == message.created_at

        mock_send_message_to_conversation.assert_called_once_with(
            message_obj=message,
            conversation=conversation,
        )

    def test_send_group_message_unauthenticated(self, api_client):
        url = reverse(RouteNames.Messaging.SENDGROUPMESSAGE)

        request_payload = {
            "message_type": "message.send",
            "conversation_id": "00000000-0000-0000-0000-000000000000",
            "content": "Hello, team!",
            "idempotency_key": "c97c9e8c-3f28-4f5f-8daf-7b3cb2783f5c",
        }

        response = api_client.post(
            url,
            data=request_payload,
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED



    def test_send_group_message_invalid_data(
        self,
        api_client,
        user_factory,
        conversation_factory,
        conversation_participant_factory):
        url = reverse(RouteNames.Messaging.SENDGROUPMESSAGE)

        sender = user_factory(
            first_name="John",
            last_name="Doe",
        )

        conversation = conversation_factory(
            conversation_type="GROUP",
            group_name="Backend Engineers",
        )
        

        conversation_participant_factory(
            conversation=conversation,
            user=sender,
        )

        api_client.force_authenticate(user=sender)

        request_payload = {
            "message_type": "message.send",
            "conversation_id": str(conversation.id),
            "idempotency_key": "c97c9e8c-3f28-4f5f-8daf-7b3cb2783f5c",
        }

        response = api_client.post(
            url,
            data=request_payload,
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert response.data["message"] == "Message content is required"


    def test_create_message_success(
        self,
        conversation_factory,
        user_factory
        ):
        conversation = conversation_factory(
            conversation_type="GROUP",
            group_name="Backend Engineers")
        sender = user_factory()

        idempotency_key = uuid.uuid4()
        content = "Hello, team!"

        message, created = MessageRepository.create_message(
            conversation_id=conversation.id,
            sender_id=sender.id,
            content=content,
            idempotency_key=idempotency_key,
        )

        assert created is True
        assert message is not None
        assert message.conversation_id == conversation.id
        assert message.sender_id == sender.id
        assert message.content == content
        assert message.idempotency_key == idempotency_key



    def test_create_message_returns_existing_message_for_duplicate_idempotency_key(
        self,
        user_factory,
        conversation_factory
        ):
        sender = user_factory()
        conversation = conversation_factory()

        idempotency_key = uuid.uuid4()

        first_message, first_created = MessageRepository.create_message(
            conversation_id=conversation.id,
            sender_id=sender.id,
            content="Hello, team!",
            idempotency_key=idempotency_key,
        )

        # Second call uses the same idempotency key
        second_message, second_created = MessageRepository.create_message(
            conversation_id=conversation.id,
            sender_id=sender.id,
            content="This should not create a new message",
            idempotency_key=idempotency_key,
        )

        assert first_created is True
        assert second_created is False

        assert second_message.id == first_message.id
        assert second_message.idempotency_key == idempotency_key

        assert second_message.content == "Hello, team!"

        assert Message.objects.filter(
            conversation=conversation,
            sender=sender,
            idempotency_key=idempotency_key,
        ).count() == 1


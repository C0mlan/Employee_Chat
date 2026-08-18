import pytest
from apps.messaging.serializers import CreateGroupConversationSerializer
import uuid
import pytest
from unittest.mock import patch

from apps.messaging.services.conversation_services import ConversationService
from common.constants.conversation_type import Type
from common.apiexceptions.messaging import InvalidParticipant, DuplicateParticipant
from common.constants.status import Status
import secrets

@pytest.mark.unit
class TestGroupConversationunit:

    def test_create_group_conversation_serializer_accepts_valid_participants(self, regular_user, create_user):
        user1 = create_user(
            first_name="jane",
            last_name="doe",
            email="another@user1.com",
            password= "StrongPassword123",
            emp_id=secrets.token_hex(4),

        )

        user2 = create_user(
            first_name="john",
            last_name="doe",
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

        request = type(
            "Request",
            (),
            {"user": regular_user},
        )()

        serializer = CreateGroupConversationSerializer(
            data=data,
            context={"request": request},
        )

        assert serializer.is_valid() is True

        assert serializer.validated_data["group_name"] == "Engineering Team"

        assert serializer.validated_data["participant_ids"] == [
            user1, user2
        ]

    @patch(
        "apps.messaging.services.conversation_services.ConversationRepository.create_conversation"
    )
    def test_create_group_conversation_service(self, mock_create_conversation,regular_user):
        participant_ids = [2, 3, 4]
        group_name = "Engineering Team"
        description = "Engineering department group"

        expected_conversation = object()
        mock_create_conversation.return_value = expected_conversation

        result = ConversationService.create_group_conversation(
            creator=regular_user,
            participant_ids=participant_ids,
            group_name=group_name,
            description=description,
        )

        mock_create_conversation.assert_called_once_with(
            conversation_type=Type.GROUP,
            group_name=group_name,
            description=description,
            creator=regular_user,
            participants=participant_ids,
        )

        assert result is expected_conversation
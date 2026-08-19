import pytest
from common.validators.messaging.conversation_validators import CreateConversationValidators
import uuid
from common.apiexceptions.messaging import (InvalidParticipant,DuplicateParticipant, CannotAddSelf)

@pytest.mark.unit
class TestConversationValidators:

    def test_validate_group_ids_rejects_fewer_than_two_participants(self, regular_user):
        participant_ids = []

        with pytest.raises(
            InvalidParticipant,
            match="A group must have at least 2 other participants."):
            
            CreateConversationValidators.validate_group_ids(
                participant_ids,
                regular_user,
            )

    def test_validate_group_ids_rejects_duplicate_participant_ids(self,regular_user):
        participant_id = uuid.uuid4()
        participant_ids = [
            participant_id,
            participant_id
        ]

        with pytest.raises(
            DuplicateParticipant,
            match= "Participant IDs must be unique."
        ):
            CreateConversationValidators.validate_group_ids(
                participant_ids,
                regular_user,
            )

    def test_validate_group_ids_rejects_self(self, regular_user):
        participant_one = uuid.uuid4()
        participant_two = uuid.uuid4()

        participant_ids = [
            regular_user.id,
            participant_one,
            participant_two
        ]

        with pytest.raises(
            CannotAddSelf,
            match= "You cannot add yourself as a participant."
        ):
            CreateConversationValidators.validate_group_ids(
                participant_ids,
                regular_user,
            )
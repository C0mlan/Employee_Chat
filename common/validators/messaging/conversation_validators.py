"""Validation rules for data used when creating conversations through serializers."""

from apps.messaging.repositories.conversation_repositories import ConversationRepository
from common.apiexceptions.messaging import (InvalidParticipantCount,
 InvalidGroupName, 
 DuplicateParticipant,
 CannotAddSelf,
 InvalidParticipant)

class CreateConversationValidators:
            
    @staticmethod
    def validate_group_name(group_name: str) -> str:
        if not group_name:
            raise InvalidGroupName(
                "Group name is required for group conversations."
            )

        group_name = group_name.strip()

        if len(group_name) < 3:
            raise InvalidGroupName(
                "Group name must be at least 3 characters long."
            )
        return group_name

    @staticmethod
    def validate_group_ids(participant_ids, user):
        """Validate participant IDs: no duplicates, all exist, all active, not self."""

        if len(participant_ids) < 2:
            raise InvalidParticipant(
                "A group must have at least 2 other participants."
            )

        participant_set = set(participant_ids)
        if len(participant_ids) != len(participant_set):
            raise DuplicateParticipant()
        if user.id in participant_set:
            raise CannotAddSelf("You cannot add yourself as a participant.")
        participants = list(ConversationRepository.get_active_users_by_ids(
            participant_ids)
            )
        found_ids = {p.id for p in participants}
        missing_ids = participant_set - found_ids

        if missing_ids:
            raise InvalidParticipant(
                f"Some participants are invalid or inactive: {missing_ids}"
            )

        return participants


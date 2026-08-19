from django.db import transaction
from apps.messaging.repositories.conversation_repositories import ConversationRepository
from common.constants.conversation_type import Type
from common.apiexceptions.messaging import InvalidParticipant

class ConversationService:

    @staticmethod
    @transaction.atomic
    def create_group_conversation(*, creator, participant_ids, group_name, description=None):

        return ConversationRepository.create_conversation(
            conversation_type=Type.GROUP,
            group_name=group_name,
            description=description,
            creator=creator,
            participants=participant_ids)
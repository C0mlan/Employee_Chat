from django.db import transaction
from django.contrib.auth import get_user_model
from apps.messaging.models import Conversation, ConversationParticipant
from common.constants.status import Status
from uuid import UUID

User = get_user_model()

class ConversationRepository:
    @staticmethod
    def create_conversation(*, conversation_type,group_name,description=None, creator, participants):
        """Create a group conversation with multiple participants."""
        participants = list(participants)

        if creator not in participants:
            participants.append(creator)
        conversation = Conversation.objects.create(
            conversation_type=conversation_type,
            group_name=group_name,
            description=description,
            created_by=creator)
         
        # Add creator + all participants
        ConversationParticipant.objects.bulk_create([
            ConversationParticipant(conversation=conversation, user=user)
            for user in participants
        ])
        
        return conversation

    @staticmethod
    def get_active_users_by_ids(participant_ids):
        return User.objects.filter(
            id__in=participant_ids,
            status__in=[
            Status.ACTIVE,
            Status.SUSPENDED,
            ],
        )
    @staticmethod
    def get_conversation_by_id(conversation_id: UUID) -> Conversation | None:
        return Conversation.objects.filter(id=conversation_id).first()

    @staticmethod
    def get_participant_user_ids(conversation_id: str | UUID) -> list[UUID]:
        """
        Return a list of user UUIDs who are participants in the given conversation.
        """
        conversation_id = str(conversation_id)

        qs: QuerySet = (
            ConversationParticipant.objects
            .filter(conversation_id=conversation_id)
            .values_list("user_id", flat=True)
        )
        return list(qs)
    @staticmethod
    def update_last_message(conversation, message):
        conversation.last_message_id = message.id
        conversation.last_message_at = message.created_at
        conversation.save(update_fields=["last_message_id","last_message_at",])
        return conversation
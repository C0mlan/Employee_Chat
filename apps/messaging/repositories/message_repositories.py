from apps.messaging.models import Message
from uuid import UUID
from typing import Tuple

class MessageRepository:
    """Repository layer for persisting and querying Message domain models.

    Encapsulates direct database operations related to chat messages.
    """
    @staticmethod
    def create_message(conversation_id: UUID, sender_id: UUID,content: str,idempotency_key: UUID) -> Tuple[Message, bool]:
        """Creates or fetches a message using an idempotency key to prevent duplication.

        Queries the database for an existing message matching the conversation,
        sender, and idempotency key. If found, returns the existing instance;
        otherwise, creates a new message record with the provided content.

        Args:
            conversation_id: UUID identifying the target conversation.
            sender_id: UUID identifying the message sender.
            content: The body text content of the message.
            idempotency_key: Unique UUID preventing duplicate message creation.

        Returns:
                - message_obj (Message): The persisted or retrieved Message instance.
                - created (bool): True if a new message was created, False if retrieved.
        """
        message_obj, created = Message.objects.get_or_create(
            conversation_id=conversation_id,
            sender_id=sender_id,
            idempotency_key=idempotency_key,
            defaults={"content": content},
        )
        return message_obj, created

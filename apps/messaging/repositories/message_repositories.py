from apps.messaging.models import Message
from uuid import UUID
from typing import Tuple

class MessageRepository:
    @staticmethod
    def create_message(conversation_id: UUID, sender_id: UUID,content: str,idempotency_key: UUID) -> Tuple[Message, bool]:
        message_obj, created = Message.objects.get_or_create(
            conversation_id=conversation_id,
            sender_id=sender_id,
            idempotency_key=idempotency_key,
            defaults={"content": content},
        )
        return message_obj, created 

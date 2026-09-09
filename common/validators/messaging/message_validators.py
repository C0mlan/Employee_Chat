
from uuid import UUID
from apps.messaging.repositories.conversation_repositories import ConversationRepository
from common.constants.message_type import MessageEventType
from typing import Optional, Any
from common.apiexceptions.messaging import (InvalidMessageType, 
InvalidConversationId,
InvalidMessageContent,
InvalidIdempotencyKey,

)

class MessageValidators:

    @staticmethod
    def validate_message_serializers(data: dict) -> dict:
        """Validate and normalize the full serializer input payload.

        Args:
            data: Raw validated_data dict from the serializer.

        Returns:
            The same dict with fields normalized and validated.

        Raises:
            InvalidMessageContent: If message_type or content is missing/invalid.
            InvalidConversationId: If conversation_id is missing.
            InvalidIdempotencyKey: If idempotency_key is missing.
            InvalidMessageType: If message_type is not in allowed values.
        """
        if "message_type" not in data or data["message_type"] is None:
            raise InvalidMessageContent("Message content is required.")
        
        MessageValidators._validate_message_type(data["message_type"])
        data.pop("message_type")
        
        if "conversation_id" not in data or data["conversation_id"] is None:
            raise InvalidConversationId("Conversation ID is required.")
        

        if "idempotency_key" not in data or data["idempotency_key"] is None:
            raise InvalidIdempotencyKey("Idempotency key is required.")

        if "content" not in data or data["content"] is None or data["content"].strip() == "":
            raise InvalidMessageContent("Message content is required.")
        data["content"] = MessageValidators._validate_content(data["content"])

        return data

    @staticmethod
    def _validate_message_type(value: str) -> str:
        if value not in MessageEventType.VALUES:
            raise InvalidMessageType
        return value

    @staticmethod
    def _validate_content(value: str, file: Optional[Any] = None, require_file: bool = False) -> str:
        value = value.strip()
        if len(value) > 500:
            raise InvalidMessageContent("Message cannot exceed 500 characters.")

        if require_file and file is None:
            raise InvalidMessageContent("A file is required.")
        return value
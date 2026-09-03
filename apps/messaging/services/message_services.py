from apps.messaging.repositories.conversation_repositories import ConversationRepository
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.messaging.repositories.message_repositories import MessageRepository
from common.apiexceptions.messaging import ConversationNotFound
from django.db import transaction
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class MessageService:
    @staticmethod
    def create_and_send_message(conversation_id: str, content: str, idempotency_key:UUID, sender_id:UUID):
        conversation =  ConversationRepository.get_conversation_by_id(conversation_id)
        if not conversation:
            logger.warning("Conversation not found: %s", conversation_id, 
            extra={"user_id": str(sender_id)},)
            raise ConversationNotFound("Conversation not found")
        
        message_obj, created = MessageRepository.create_message(
            conversation_id=conversation_id,sender_id=sender_id,content=content,idempotency_key=idempotency_key)
        if not created:
            logger.info("Message request already processed",
                extra={
                    "message_id": str(message_obj.id),
                    "conversation_id": str(conversation_id),
                    "user_id": str(sender_id),
                    "idempotency_key": str(idempotency_key),
                },
            )
        logger.info("Message created",
            extra={
                "message_id": str(message_obj.id),
                "conversation_id": str(conversation_id),
                "user_id": str(sender_id),
            },
        )
        transaction.on_commit(
            lambda: MessageService._send_message_to_conversation(
                message_obj=message_obj,
                conversation=conversation
            )
        )
        logger.info("Message delivery scheduled",
            extra={
                "message_id": str(message_obj.id),
                "conversation_id": str(conversation_id),
                "user_id": str(sender_id),
            },
        )
        return message_obj, created
      
       
    @staticmethod
    def _send_message_to_conversation(message_obj, conversation):
        channel_layer = get_channel_layer()
        group_name = f"conversation_{message_obj.conversation_id}"
        payload = {
            "type": "chat_message", 
            "message": {
                "message_id": str(message_obj.id),
                "conversation_id": str(message_obj.conversation_id),
                "sender_id": str(message_obj.sender_id),
                "content": message_obj.content,
                "conversation_type": str(conversation.conversation_type),
                "created_at": message_obj.created_at.isoformat()
            },
        }
        try:
            async_to_sync(channel_layer.group_send)(group_name, payload)
            logger.info("Message sent to conversation",
            extra={
                "message_id": str(message_obj.id),
                "conversation_id": str(message_obj.conversation_id),
                "user_id": str(message_obj.sender_id),
                "conversation_type": str(conversation.conversation_type),
                },
            )
        except Exception:
            logger.exception("Failed to send message to conversation",
                extra={
                    "message_id": str(message_obj.id),
                    "conversation_id": str(message_obj.conversation_id),
                    "user_id": str(message_obj.sender_id),
                    "conversation_type": str(conversation.conversation_type),
                },
            )
            raise
        

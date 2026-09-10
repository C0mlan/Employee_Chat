from apps.messaging.repositories.conversation_repositories import ConversationRepository
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.messaging.repositories.message_repositories import MessageRepository
from common.apiexceptions.messaging import ConversationNotFound
from apps.messaging.tasks import group_message_pushes_async
from django.db import transaction
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class MessageService:
    """Service layer handling message creation, real-time dispatches, and background tasks."""
    @staticmethod
    @transaction.atomic
    def create_and_send_group_message(conversation_id: str, content: str, idempotency_key:UUID, sender_id:UUID):
        """Creates a group message record and schedules real-time delivery post-commit.

        Validates conversation existence, creates or retrieves the message via
        idempotency key, and registers a post-transaction hook to push the message
        over WebSocket channels and push notification queues.

        Args:
            conversation_id: Unique string identifier for the target conversation.
            content: The message body text.
            idempotency_key: UUID token preventing duplicate message creation.
            sender_id: UUID of the authenticated user sending the message.

        Returns:
                - message_obj (Message): The created or existing Message model instance.
                - created (bool): True if a new record was created, False if returned via idempotency.

        Raises:
            ConversationNotFound: If no conversation matches `conversation_id`.
        """
        conversation = (ConversationRepository.get_conversation_by_id(conversation_id))
        
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
            return message_obj, False
        ConversationRepository.update_last_message(conversation=conversation,message=message_obj)
        
        logger.info("Message created and conversation updated",
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
        """Broadcasts a message payload to a channel layer group via WebSockets.

        Dispatches real-time WebSocket events to connected conversation members.
        Triggers group push notification batching if the conversation type is 'GROUP'.

        Args:
            message_obj: The Message database model instance to send.
            conversation: The Conversation database model instance.

        """
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
        
        if conversation.conversation_type == "GROUP": 
            MessageService._batch_group_pushes(message_obj, conversation)

    @staticmethod
    def _batch_group_pushes(message_obj, conversation):
        """Enqueues an asynchronous Celery task to send push notifications.

        Extracts metadata (sender name, group title, truncated message preview)
        and dispatches the job to background workers via Celery.

        Args:
            message_obj: The Message database model instance containing sender and content.
            conversation: The Conversation database model instance representing the group.
        """
        sender_name = getattr(message_obj.sender, "first_name", "") or ""
        message_preview = (message_obj.content or "")[:100]
        group_name = getattr(conversation, "name", "") or ""

        result = group_message_pushes_async.delay(
            sender_id=str(message_obj.sender_id),
            conversation_id=str(conversation.id),
            message_id=str(message_obj.id),
            sender_name=sender_name,
            message_preview=message_preview,
            group_name=group_name,
        )

"""
Celery tasks for async session
All tasks are idempotent and retry-safe.
"""

import logging
from uuid import UUID

from celery import shared_task, Task
from django.utils import timezone
from django.db import DatabaseError

# from config.notification.novu_service import novu_service
# from apps.accounts.redis_client import redis_client
# from config.notification.novu_service import novu_service
from apps.messaging.models import Message, Conversation 
from apps.messaging.repositories.conversation_repositories import ConversationRepository

logger = logging.getLogger(__name__)


class BaseTask(Task):
    """
    Base task class with common retry configuration.
    """
    autoretry_for = (DatabaseError, Exception)
    retry_backoff = True
    retry_backoff_max = 300  # Cap retry delay at 5 minutes
    retry_kwargs = {"max_retries": 5}
    default_retry_delay = 10  # Start with 10 seconds




@shared_task(bind=True, base=BaseTask)
def group_message_pushes_async(
    self,
    sender_id,
    conversation_id: str,
    message_id: str,
    sender_name: str,
    message_preview: str,
    group_name: str,
    ) -> None:
    """Dispatches asynchronous push notifications to group message recipients.

    Fetches group participants from the repository, filters out the message sender,
    and enqueues push notifications via the Novu notification service for all
    remaining recipients.

    Args:
        self: The bound Celery Task instance context.
        sender_id: UUID string of the user who sent the message.
        conversation_id: Unique UUID string identifying the target conversation.
        message_id: Unique UUID string identifying the sent message.
        sender_name: Display name of the sender.
        message_preview: Truncated text preview of the message content.
        group_name: Title of the group conversation.

    Returns:
        None

    Raises:
        DatabaseError: Raised on database query failures, triggering automatic task retry.
        Exception: Catches unhandled errors for logging and task retries.
    """# Re-fetch objects inside the task
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except (Message.DoesNotExist, Conversation.DoesNotExist):
        logger.warning(
            "Message or conversation not found for push task",
            extra={
                "message_id": message_id,
                "conversation_id": conversation_id,
            },
        )
        return

    participant_ids = ConversationRepository.get_participant_user_ids(conversation.id)

    logger.info("Group participants found: %s",[str(user_id) for user_id in participant_ids])
    recipient_ids = [
        uid for uid in participant_ids if uid != UUID(sender_id)
    ]

    for user_id in recipient_ids:
        try:
            # novu_service.send_group_message_push(
            #     user_id=user_id,
            #     conversation_id=conversation.id,
            #     message_id=message_id,  
            #     sender_name=sender_name,
            #     message_preview=message_preview,
            #     group_name=group_name,
            # )
            logger.info(
                "Group message push sent: user=%s, group=%s, message_id=%s",
                user_id,
                group_name,
                message_id,
            )

        except Exception:
            logger.exception(
                "Failed to send group push for message",
                extra={
                    "message_id": message_id,
                    "conversation_id": conversation.id,
                    "recipient_user_id": str(user_id),
                },
            )
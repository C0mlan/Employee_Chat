import json
import logging
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from apps.messaging.models import ConversationParticipant

logger = logging.getLogger(__name__)

# from .models import Message

@sync_to_async
def _check_participant_sync(conversation_id, user_id):
    return ConversationParticipant.objects.filter(
        conversation_id=conversation_id,
        user_id=user_id,
    ).exists()

class ChatConsumer(AsyncWebsocketConsumer):
    """Manages real-time WebSocket connections for group and direct chat conversations.

    Handles connection lifecycle hooks, user authorization validation, incoming client frame
    parsing, channel group subscription management, and error handling.

    Attributes:
        CLOSE_NORMAL (int): Standard WebSocket closure code (1000).
        CLOSE_GOING_AWAY (int): Endpoint going away code (1001).
        CLOSE_PROTOCOL_ERROR (int): Protocol error closure code (1002).
        CLOSE_UNAUTHORIZED (int): Custom closure code for unauthorized access (4003).
        CLOSE_SERVER_ERROR (int): Custom closure code for internal server errors (4011).
    """
    CLOSE_NORMAL = 1000
    CLOSE_GOING_AWAY = 1001
    CLOSE_PROTOCOL_ERROR = 1002
    CLOSE_UNAUTHORIZED = 4003
    CLOSE_SERVER_ERROR = 4011

    async def connect(self):
        """Handles new incoming WebSocket connection attempts.

        Extracts parameters from connection scope, validates conversation membership,
        and adds valid connections to the corresponding Redis/channel group.

        Returns:
            None
        """
        logger.info("1. connect() called")
        headers = dict(self.scope.get("headers", []))
        user_agent_raw = headers.get(b"user-agent", b"").decode("utf-8")
        ip_address = self.scope["client"][0] if self.scope.get("client") else None

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]

        self.conversation_group_name = f"conversation_{self.conversation_id}"
        logger.info("2. conversation_id=%s",self.conversation_id)
        self.user_id = self.scope["user_id"]
        logger.info("3. user_id=%s", self.user_id)
        if not self.conversation_id:
            logger.warning("WebSocket connection rejected: missing conversation_id",
                extra={
                    "user_id": self.user_id,
                    "browser":  user_agent_raw,
                    "ip_address": ip_address
                    },
            )
            await self.close(code=self.CLOSE_PROTOCOL_ERROR)
            return
        logger.info("4. Checking participant")
        is_participant = await self.check_participant()
        logger.info("5. Participant check completed: %s",is_participant,)

        if not is_participant:
            logger.warning(
                "WebSocket connection rejected: user not a participant",
                extra={
                    "conversation_id": self.conversation_id,
                    "user_id": self.user_id,
                    "browser":  user_agent_raw,
                    "ip_address": ip_address
                },
            )
            await self.close(code=self.CLOSE_UNAUTHORIZED)
            return
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name,
        )
        await self.accept()
        logger.info(
            "WebSocket connection accepted and added to group ",
            extra={
                "conversation_id": self.conversation_id,
                "user_id": self.user_id,
                "group_name": self.conversation_group_name,
                
            },
        )
    async def disconnect(self, close_code):
        """Handles WebSocket disconnect events and performs cleanup.

        Removes connection channel name from the group and logs the exit code.

        Args:
            close_code: Integer close code indicating why connection terminated.

        Returns:
            None
        """
        try:
            logger.info("WebSocket disconnecting",
                extra={
                    "conversation_id": getattr(self, "conversation_id", None),
                    "user_id": getattr(self, "user_id", None),
                    "close_code": close_code,
                    "channel_name": self.channel_name,
                    },
            )
            if hasattr(self, "conversation_group_name"):
                await self.channel_layer.group_discard(
                    self.conversation_group_name,
                    self.channel_name,
                )
                
        except Exception as e:
            logger.error("WebSocket disconnect cleanup failed: %s",str(e),
                extra={
                    "conversation_id": getattr(self, "conversation_id", None),
                    "user_id": getattr(self, "user_id", None),
                    },
                    exc_info=True,
            )

    async def receive(self, text_data=None, bytes_data=None):
        """Processes incoming data frames received from WebSocket clients.

        Parses raw text or byte data into JSON, validates payload structures,
        enforces max character constraints, and broadcasts frames to group layers.

        Args:
            text_data: Optional raw JSON string received from client.
            bytes_data: Optional UTF-8 encoded byte array received from client.

        Returns:
            None
        """
        try:
            # Parse incoming data
            if text_data:
                data = json.loads(text_data)
            elif bytes_data:
                data = json.loads(bytes_data.decode('utf-8'))
            else:
                logger.warning(
                    "WebSocket received empty message",
                    extra={
                        "conversation_id": str(self.conversation_id),
                        "user_id": str(self.user_id),
                    },
                )
                await self.send_json_error(
                        code="INVALID_MESSAGE",
                        message="Message cannot be empty"
                    )
                return
            if "message" not in data:
                logger.warning(
                    "WebSocket message missing 'message' field",
                    extra={
                        "conversation_id": str(self.conversation_id),
                        "user_id": str(self.user_id),
                        "data_keys": list(data.keys()) if isinstance(data, dict) else None,
                    },
                )
                await self.send_json_error(
                    code="INVALID_FORMAT",
                    message="Message must contain 'message' field"
                )
                return
            
            message = data["message"]
            if isinstance(message, dict) and "content" in message:
                if len(message["content"]) > 500:
                    await self.send_json_error(
                        code="MESSAGE_TOO_LONG",
                        message="Message content exceeds maximum length"
                    )
                    return
            await self.channel_layer.group_send(
                self.conversation_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                },
                )
            
            logger.debug(
                "WebSocket message broadcast",
                extra={
                    "conversation_id": str(self.conversation_id),
                    "user_id": str(self.user_id),
                    "message_type": type(message).__name__,
                    },
                    )
        except Exception as e:
            logger.error(
                "WebSocket receive failed: %s",
                str(e),
                extra={
                    "conversation_id": str(self.conversation_id),
                    "user_id": str(self.user_id),
                },
                exc_info=True,
            )
            await self.send_json_error(
                code="INTERNAL_ERROR",
                message="Failed to process message"
            )
                

    async def chat_message(self, event):
        """Handler for channel layer group messages with type 'chat_message'.

        Serializes and pushes the broadcast message frame to the client WebSocket.

        Args:
            event: Event dictionary sent by channel layer containing message data.

        Returns:
            None
        """
        try:
            logger.info("WebSocket delivering message",
                extra={
                    "conversation_id": str(self.conversation_id),
                    "user_id": str(self.user_id),
                    "event_type": event.get("type"),
                },
            )
            
            await self.send(text_data=json.dumps({"message": event["message"],}))
            
        except Exception as e:
            logger.error(
                "WebSocket send failed: %s",
                str(e),
                extra={
                    "conversation_id": str(self.conversation_id),
                    "user_id": str(self.user_id),
                    "event_type": event.get("type"),
                },
                exc_info=True,
            )
    async def send_json_error(self, code, message):
        """Helper method to format and send structured JSON error frames to client.

        Args:
            code: Unique string code classifying error state (e.g., 'INVALID_FORMAT').
            message: Human-readable error description string.

        Returns:
            None
        """
        try:
            await self.send(
                text_data=json.dumps({
                    "type": "error",
                    "error": {
                        "code": code,
                        "message": message,
                    },
                })
            )

            logger.info(
                    "WebSocket error sent to client",
                    extra={
                        "conversation_id": str(self.conversation_id),
                        "user_id": str(self.user_id),
                        "error_code": code,
                    },
                )
        except Exception as e:
            logger.error(
                "Failed to send error to client: %s",
                str(e),
                extra={
                    "conversation_id": str(self.conversation_id),
                    "user_id": str(self.user_id),
                    "error_code": code,
                },
                exc_info=True,)


    async def check_participant(self):
        """Verifies whether the current connected user belongs to the conversation.

        Queries ConversationParticipant in a synchronous context wrapped for async.

        Returns:
            bool: True if membership record exists, False otherwise.

        Raises:
            Exception: Re-raises database access errors after logging details.
        Async wrapper around the DB check."""
        try:
            return await _check_participant_sync(self.conversation_id, self.user_id)
        except Exception as e:
            logger.error(
                "Database check_participant failed: %s",
                str(e),
                extra={
                    "conversation_id": str(self.conversation_id),
                    "user_id": str(self.user_id),
                },
                exc_info=True,
            )
            raise
       
class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        await self.send(text_data=text_data or bytes_data)
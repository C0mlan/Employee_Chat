import pytest
from channels.testing import WebsocketCommunicator
from apps.messaging.consumers import ChatConsumer
from config.asgi import application
from rest_framework_simplejwt.tokens import RefreshToken
from asgiref.sync import sync_to_async
import uuid

@pytest.mark.django_db(transaction=True)
# reset_sequences=True)
@pytest.mark.asyncio
class TestChatConsumerIntegration:

    async def test_ws_connect_success(
        self,
        websocket_test_data
        ):
        
        user, conversation = websocket_test_data
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        communicator = WebsocketCommunicator(
            application, f"/ws/conversations/{conversation.id}/", 
            headers=[(b"authorization", f"Bearer {access_token}".encode())],)
        connected, _ = await communicator.connect()

        assert connected is True

        await communicator.disconnect()

        

    @pytest.mark.asyncio
    async def test_ws_connect_non_participant(
        self,
        user_factory,
        conversation_factory,
        conversation_participant_factory
        ):
        participant = await sync_to_async(user_factory)( first_name="John", last_name="Doe", )

        non_participant = await sync_to_async(user_factory)( first_name="Jane", last_name="Doe", )

        conversation = await sync_to_async(conversation_factory)( conversation_type="GROUP", group_name="Backend Engineers", )
        await sync_to_async(conversation_participant_factory)( conversation=conversation, user=participant, )

        refresh = RefreshToken.for_user(non_participant)
        access_token = str(refresh.access_token)

        communicator = WebsocketCommunicator(
            application,
            f"/ws/conversations/{conversation.id}/",
            headers=[
                (b"authorization", f"Bearer {access_token}".encode()),
            ],
        )

        connected, _ = await communicator.connect()

        assert connected is False


    @pytest.mark.asyncio
    async def test_ws_receive_empty_message(self, websocket_test_data):
        user, conversation = websocket_test_data

        refresh = await sync_to_async(RefreshToken.for_user)(user)
        access_token = str(refresh.access_token)

        communicator = WebsocketCommunicator(
            application,
            f"/ws/conversations/{conversation.id}/",
            headers=[
                (b"authorization", f"Bearer {access_token}".encode()),
            ],
        )

        connected, _ = await communicator.connect()

        assert connected is True

        await communicator.send_json_to({
            "message_type": "message.send",
            "conversation_id": str(conversation.id),
            "content": "",
            "idempotency_key": str(uuid.uuid4()),
        })

        response = await communicator.receive_json_from()

        assert response["type"] == "error" 
        assert response["error"]["code"] == "INVALID_FORMAT" 
        assert response["error"]["message"] == "Message must contain 'message' field"

        await communicator.disconnect()


    @pytest.mark.asyncio
    async def test_ws_receive_exceeds_max_length(self, websocket_test_data):
        user, conversation = websocket_test_data

        refresh = await sync_to_async(RefreshToken.for_user)(user)
        access_token = str(refresh.access_token)

        communicator = WebsocketCommunicator(
            application,
            f"/ws/conversations/{conversation.id}/",
            headers=[
                (b"authorization", f"Bearer {access_token}".encode()),
            ],
        )

        connected, _ = await communicator.connect()

        assert connected is True

        message = {
            "message": {
                "content": "a" * 501,
            }
        }

        await communicator.send_json_to(message)

        response = await communicator.receive_json_from()

        assert response["type"] == "error"
        assert response["error"]["code"] == "MESSAGE_TOO_LONG"
        assert response["error"]["message"] == "Message content exceeds maximum length"

        await communicator.disconnect()


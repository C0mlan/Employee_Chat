from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateGroupConversationSerializer
from .services.conversation_services import ConversationService
from common.response.authcore_response import  MessagingResponses
from rest_framework.permissions import IsAuthenticated
from .permissions import CanCreateGroup

import logging


logger = logging.getLogger(__name__)


class CreateConversationAPI(APIView):
    permission_classes = [CanCreateGroup]

    def post(self, request):
        serializer = CreateGroupConversationSerializer(data=request.data, context={"request": request},)
        serializer.is_valid(raise_exception=True)

        conversation = ConversationService.create_group_conversation(
            creator=request.user,
            **serializer.validated_data
            )

        return  MessagingResponses.conversation_created(
            data={
            'id': conversation.id,
            'type': conversation.conversation_type,
            'group_name': conversation.group_name,
            'participant_count': conversation.participants.count()})
from .serializers import SendMessageSerializer
from .services.message_services import MessageService

class SendGroupMessage(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["sender_id"] = request.user.id
        message_obj, created = MessageService.create_and_send_message(**data)
        return Response(
            {
                "status": True,
                "message_id": str(message_obj.id),
                "created": created,
                "created_at": message_obj.created_at.isoformat(),}, status=status.HTTP_200_OK)
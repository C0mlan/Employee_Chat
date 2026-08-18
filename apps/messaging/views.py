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
from rest_framework import serializers
from common.validators.messaging.conversation_validators import CreateConversationValidators
from common.validators.messaging.message_validators import MessageValidators

class CreateGroupConversationSerializer(serializers.Serializer):
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=True,
    )
    group_name = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, trim_whitespace=True,)
    
    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    def validate(self, data):
        request = self.context["request"]
        user = request.user
        participant_ids = data.get("participant_ids", [])
        validated_ids = CreateConversationValidators.validate_group_ids(participant_ids, user)
        data["participant_ids"] = validated_ids
        return data

    def validate_group_name(self, value):
        return CreateConversationValidators.validate_group_name(value)

class SendGroupMessageSerializer(serializers.Serializer):
    """Serializes and validates incoming message payload data.

    Attributes:
        message_type: Required event type identifier. Must be 'message.send'.
        conversation_id: UUID identifying the target conversation.
        content: text content of the message.
        idempotency_key: UUID used to prevent duplicate message creation.
    """
    message_type = serializers.CharField( required=False, allow_blank=True, allow_null=True)
    conversation_id = serializers.UUIDField(required=False, allow_null=True)
    content = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    idempotency_key = serializers.UUIDField(required=False,allow_null=True)

    def validate(self, data: dict) -> dict:
        return MessageValidators.validate_message_serializers(data)


    


    
        

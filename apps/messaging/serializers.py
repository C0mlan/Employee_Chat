from rest_framework import serializers
from common.validators.messaging.conversation_validators import CreateConversationValidators

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

    
        

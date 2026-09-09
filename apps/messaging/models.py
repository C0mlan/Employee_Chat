from django.db import models
from django.conf import settings
import uuid
from django.db import models
from django.conf import settings
from common.constants.conversation_status import Status
from common.constants.conversation_type import Type



class Conversation(models.Model):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
        
    conversation_type = models.CharField(
        max_length=20, choices=Type.CHOICES, default=Type.DIRECT)
    
    group_name = models.CharField(
        max_length=100, null=True, blank=True)

    description = models.TextField(
            null=True,
            blank=True,
        )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_conversation')
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(null=True,blank=True)
    
    last_message_id = models.UUIDField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=Status.CHOICES, default=Status.ACTIVE)

    class Meta:
        db_table = 'conversations'
        ordering = ['-last_message_id']
        indexes = [
            models.Index(fields=['created_by']),
            models.Index(fields=['status']),
        ]

        def __str__(self):
            return f"Conversation {self.id} ({self.conversation_type})"

        
class ConversationParticipant(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.SET_NULL, null=True, related_name="participants")
    user =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="conversation_participations")
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read_message = models.ForeignKey(
        "Message",on_delete=models.SET_NULL,null=True,blank=True,related_name="+",
        )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["conversation", "user"],
                name="unique_conversation_participant",
            ),
        ]


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE,related_name="messages")
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="sent_messages")
    content = models.TextField()
    idempotency_key = models.UUIDField(unique=True, db_index=True,default=uuid.uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['conversation', 'sender', 'idempotency_key'],
                name='unique_message_per_conversation_sender_idempotency'
            )
        ]
        indexes = [
            models.Index(
                fields=["conversation", "-created_at"],
                name="message_convo_created_idx",
            ),
        ]
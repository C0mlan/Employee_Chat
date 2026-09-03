from django.urls import path, include
from .views import CreateConversationAPI, SendGroupMessage

urlpatterns = [
    path('conversations/group/',  CreateConversationAPI.as_view(), name="create_group_conversation"),
    path('send_message/',  SendGroupMessage.as_view(), name="send_message"),
   
]
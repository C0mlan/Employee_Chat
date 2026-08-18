from django.urls import path, include
from .views import CreateConversationAPI

urlpatterns = [
    path('conversations/group/',  CreateConversationAPI.as_view(), name="create_group_conversation"),
   
]
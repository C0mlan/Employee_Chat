from django.urls import path, include
from authcore.views.auth_view import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register")
]
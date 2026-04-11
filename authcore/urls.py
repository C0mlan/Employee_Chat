from django.urls import path, include
from authcore.views.auth_view import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('loginauth/', LoginView.as_view(), name="login")
]
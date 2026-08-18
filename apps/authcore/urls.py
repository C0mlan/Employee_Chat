from django.urls import path, include
from .views import RegisterEmployeeView, LoginView

urlpatterns = [
    path('register/', RegisterEmployeeView.as_view(), name="register"),
    path('loginauth/', LoginView.as_view(), name="employee-login")
   
]
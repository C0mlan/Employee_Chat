from django.urls import path, include
from .views import RegisterEmployeeView

urlpatterns = [
    path('register/', RegisterEmployeeView.as_view(), name="register")
   
]
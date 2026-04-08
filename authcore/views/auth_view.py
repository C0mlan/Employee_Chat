from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers.auth_serializer import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # create user instance
            response_data = {
                "message": "User created successfully",
                "id": user.id,
                "emp_id": user.emp_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "is_verified": user.is_verified,
                "role": user.role,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from ..services import generate_jwt, invalidate_jwt
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate

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

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(username=email, password=password)
        if not user:
            return Response(
                {"message": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = generate_jwt(user)
        
        return Response({
            "message": "Login successful",
            "access": token["access_token"],
            "refresh": token["refresh_token"],
            "email": user.email,
            "Emp_id": user.emp_id
           
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({"message": "Authorization header missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = auth_header.split(" ")[1]
            invalidate_jwt(token)
        except Exception:
            pass
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from .services.auth_services import AuthService
from .services.permissions import  IsAdmin
from rest_framework.response import Response
from common.response.authcore_response import AuthenticationResponses
from rest_framework.views import APIView


class RegisterEmployeeView(APIView):
    permission_classes = [IsAdmin]

    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.create_employee(serializer.validated_data)
        return AuthenticationResponses.employee_registered(
            { 
                "emp_id": user.emp_id}
            )


class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = AuthService.login_user(**serializer.validated_data)
       
        return AuthenticationResponses.login_successful(
            {
                "access": tokens["access"],
                "refresh": tokens["refresh"],
            }
         )

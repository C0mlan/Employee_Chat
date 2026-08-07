from rest_framework.views import APIView
from .serializers import RegisterSerializer
# from rest_framework.permissions import IsAuthenticated
from .services.auth_services import AuthService
from rest_framework.response import Response
from common.response.authcore_response import AuthenticationResponses
from rest_framework.views import APIView


class RegisterEmployeeView(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.create_employee(serializer.validated_data)
        return AuthenticationResponses.employee_registered(
            { 
                "emp_id": user.emp_id}
            )
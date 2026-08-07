from rest_framework.response import Response
from rest_framework import status


class ApiSuccessResponse:

    @staticmethod
    def build(
        message,
        data=None,
        status_code=status.HTTP_200_OK,
        response_code=None
    ):
        return Response(
            {
                "success": True,
                "message": message,
                "response_code": response_code,
                "data": data,
                "status_code": status_code,
            },
            status=status_code
        )

class AuthenticationResponses:

    @staticmethod
    def employee_registered(data):
        return ApiSuccessResponse.build(
            message="Employee registered successfully.",
            response_code="USER_CREATED",
            data=data,
            status_code=status.HTTP_201_CREATED,
        )

    @staticmethod
    def login_successful(data):
        return ApiSuccessResponse.build(
            message="Login successful.",
            response_code="LOGIN_SUCCESS",
            data=data,
            status_code=status.HTTP_200_OK,
        )
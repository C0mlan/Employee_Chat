import pytest
from rest_framework.test import APIRequestFactory

from common.apiexceptions.authcore import (
    custom_exception_handler,
    EmailRequired,
)

factory = APIRequestFactory()


@pytest.mark.unit
class TestApiException: 

    def test_custom_exception_handler_formats_response(self):
        request = factory.get("/")

        response = custom_exception_handler(
            EmailRequired(),
            {"request": request}
        )

        assert response.status_code == 400
        assert response.data == {
            "success": False,
            "message": "Email is required.",
            "errors": {"detail": "Email is required."},
            "status_code": 400,
        }
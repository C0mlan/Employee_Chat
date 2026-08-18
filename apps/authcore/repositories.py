from django.db import connection
from django.contrib.auth import get_user_model

Employee = get_user_model()

class EmployeeRepository:


    @staticmethod
    def exists_by_email(email: str):
        return Employee.objects.filter(
            email=email
        ).exists()

    @staticmethod
    def create_employee(**data):
        return Employee.objects.create_user(**data)

    @staticmethod
    def get_next_employee_number():
        with connection.cursor() as cursor:
            cursor.execute("SELECT nextval('employee_number_seq')")
            return cursor.fetchone()[0]
from authcore.repositories import EmployeeRepository
from common.validators.authcore.email_validator import EmailValidator
from django.utils import timezone
from django.db import transaction




class AuthService:

    @staticmethod
    def _validate_employee_email(data):
        email = data.get("email")
        # uniqueness checks
        EmailValidator.validate_email_uniqueness(email)
    
    @staticmethod
    @transaction.atomic
    def create_employee(data):
        AuthService._validate_employee_email(
            data
        )
        data.pop("confirm_password", None)
        return EmployeeRepository.create_employee(emp_id = AuthService._generate_emp_id(),
            **data
        )

    @staticmethod
    def _generate_emp_id():
        """
        Generates a unique EMP ID in the format EMP-YEAR-NNN
        Uses a DB transaction and row-level lock to avoid race conditions.
        """
       
        year = timezone.now().year
        number =  EmployeeRepository.get_next_employee_number()

        return f"EMP-{year}-{number:05d}"


    
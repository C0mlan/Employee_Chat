from apps.authcore.repositories import EmployeeRepository
from django.contrib.auth import authenticate
from common.validators.authcore.email_validator import EmailValidator
from common.apiexceptions.authcore import InvalidCredentials
from django.utils import timezone
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken



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

    @staticmethod
    def login_user(email, password):
        user = EmployeeRepository.exists_by_email(email)
        if not user:
            raise InvalidCredentials()

        auth_user = authenticate(email=email, password=password)

        if not auth_user:
            raise InvalidCredentials()

        tokens = AuthService._generate_tokens(auth_user)

        return tokens

    @staticmethod
    def _generate_tokens(user):
        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        access = refresh.access_token
        return{
            "access": str(access),
            "refresh": str(refresh)
        }
    
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import uuid
from datetime import datetime
from common.constants.roles import Roles
from common.constants.status import Status
from common.constants.department import Department


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        # Normalize the email (lowercasing the domain part) … 
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields["role"] = Roles.ADMIN
        extra_fields["dept"] = Department.EXEMPT
        
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emp_id = models.CharField(max_length=20, unique=True, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30) 
    last_name = models.CharField(max_length=30) 
    role = models.CharField(max_length=20, choices=Roles.CHOICES, default='Roles.EMPLOYEE')
    dept = models.CharField(max_length=25, choices=Department.CHOICES, default='Department.ENGINEERING')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=20,choices=Status.CHOICES, default=Status.ACTIVE)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.emp_id})"
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import uuid
from datetime import datetime


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
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emp_id = models.CharField(max_length=20, unique=True, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30) 
    last_name = models.CharField(max_length=30) 
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.emp_id})"

    def save(self, *args, **kwargs):
        if not self.emp_id:
            self.emp_id = self.generate_emp_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_emp_id():
        """
        Generates a unique EMP ID in the format EMP-YEAR-NNN
        Uses a DB transaction and row-level lock to avoid race conditions.
        """
        from django.utils import timezone
        year = timezone.now().year

        from django.db.models import Max
        from django.db import transaction

        with transaction.atomic():
            # Lock table for safe increment
            last_id = User.objects.filter(emp_id__startswith=f"EMP-{year}-") \
                                    .select_for_update() \
                                    .aggregate(Max('emp_id'))['emp_id__max']
            if last_id:
                last_num = int(last_id.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            return f"EMP-{year}-{str(new_num).zfill(3)}"



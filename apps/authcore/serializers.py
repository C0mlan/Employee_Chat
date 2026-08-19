from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from common.validators.authcore.email_validator import EmailValidator
from common.validators.authcore.password_validators import PasswordValidator
from common.constants.roles import Roles
from common.validators.base.enum_validator import EnumValidator



User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        return EmailValidator.validate_email(value)

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        PasswordValidator.validate_password_strength(password)
        PasswordValidator.validate_passwords_match(
            password=password,
            confirm_password=confirm_password,
        )

        return attrs

    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False,
        allow_blank=True,
        allow_null=True,)
    password = serializers.CharField(write_only=True,required=False,
        allow_blank=True,
        allow_null=True,)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        return EmailValidator.validate_login_email(value)

# class RefreshSerializer(serializers.Serializer):
#     refresh_token = serializers.CharField()
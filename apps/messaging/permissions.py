from rest_framework.permissions import BasePermission
# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed
# from . import is_token_valid, get_user_from_token
from common.constants.roles import Roles

class CanCreateGroup(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated 
            and request.user.role in [
                Roles.ADMIN,
                Roles.HR,
                Roles.TEAM_LEAD]
        )
from rest_framework.permissions import BasePermission
from common.constants.roles import Roles


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated 
            and request.user.role in [
                Roles.ADMIN,
                Roles.HR]
        )

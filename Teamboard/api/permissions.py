from rest_framework.permissions import BasePermission

from .models import Company


class IsAdminUser(BasePermission):
    """Allow access only to TeamBoard company administrators."""

    message = "Administrator access is required."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            return request.user.company.role == Company.Role.ADMIN
        except Company.DoesNotExist:
            return False

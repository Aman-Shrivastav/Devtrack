from rest_framework.permissions import BasePermission
from .models import UserProfile

class IsAdminUser(BasePermission):
    message = "An admin account is required."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "profile", None) and request.user.profile.role == UserProfile.Role.ADMIN)

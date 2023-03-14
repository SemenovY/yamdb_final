"""Users app permissions."""
from typing import Any

from django.http import HttpRequest
from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Moderator permissions."""

    def has_permission(self, request: HttpRequest, request_view: Any) -> bool:
        """View-level permission.

        Args:
            request: http request
            request_view: request view

        Returns:
            `True` if permission is granted, `False` otherwise.
        """
        return request.user.is_authenticated and request.user.is_moderator


class IsAdmin(permissions.BasePermission):
    """Administrator permissions."""

    def has_permission(self, request: HttpRequest, request_view: Any) -> bool:
        """View-level permission.

        Args:
            request: http request
            request_view: request view

        Returns:
            `True` if permission is granted, `False` otherwise.
        """
        return request.user.is_authenticated and request.user.is_admin

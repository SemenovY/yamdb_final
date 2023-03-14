"""Custom permissions."""
from typing import Any

from django.http import HttpRequest
from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Admin or read only permission."""

    def has_permission(self, request: HttpRequest, request_view: Any) -> bool:
        """View-level permission.

        Args:
            request: http request
            request_view: request view

        Returns:
            `True` if permission is granted, `False` otherwise.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(
        self,
        request: HttpRequest,
        request_view: Any,
        model_object: Any,
    ) -> bool:
        """View-level permission.

        Args:
            request: http request
            request_view: request view
            model_object: model object

        Returns:
            `True` if permission is granted, `False` otherwise.
        """
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_admin
        )


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """Author, Admin, Moderator or read only permission."""

    def has_permission(self, request: HttpRequest, request_view: Any) -> bool:
        """View-level permission.

        Args:
            request: http request
            request_view: request view

        Returns:
            `True` if permission is granted, `False` otherwise.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(
        self,
        request: HttpRequest,
        request_view: Any,
        model_object: Any,
    ) -> bool:
        """View-level permission.

        Args:
            request: http request
            request_view: request view
            model_object: model object

        Returns:
            `True` if permission is granted, `False` otherwise.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or model_object.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )

"""Users app models."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

USERNAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254


class UserRole(models.TextChoices):
    """User roles class."""

    user = ("user", _("User"))
    moderator = ("moderator", _("Moderator"))
    admin = ("admin", _("Administrator"))


class User(AbstractUser):
    """User class."""

    email = models.EmailField(
        _("email address"),
        max_length=EMAIL_MAX_LENGTH,
        blank=False,
        unique=True,
    )
    role = models.SlugField(
        _("user role"),
        choices=UserRole.choices,
        default=UserRole.user,
    )
    bio = models.TextField(_("user bio"), blank=True)

    @property
    def is_admin(self) -> bool:
        """Check if user is admin.

        Returns:
            `True` if user is admin, `False` otherwise.
        """
        return self.role == UserRole.admin or self.is_superuser

    @property
    def is_moderator(self) -> bool:
        """Check if user is moderator.

        Returns:
            `True` if user is moderator, `False` otherwise.
        """
        return self.role == UserRole.moderator

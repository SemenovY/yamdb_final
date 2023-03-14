"""Users app serializers."""
from rest_framework import serializers

from .models import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH, User


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:
        """User serializer meta."""

        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "bio",
        )


class UserCreationSerializer(serializers.Serializer):
    """User creating serializer."""

    username = serializers.SlugField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
    )
    email = serializers.EmailField(required=True, max_length=EMAIL_MAX_LENGTH)

    def validate(self, serializer_data: dict) -> dict:
        """Validate serializer data.

        Args:
            serializer_data: serializer data to be validated

        Returns:
            Serializer data

        Raises:
            ValidationError: if serializer data is not valid
        """
        if (  # noqa: WPS337
            User.objects.filter(username=serializer_data["username"]).exists()
            ^ User.objects.filter(email=serializer_data["email"]).exists()
        ):
            raise serializers.ValidationError(
                "Пользователь с таким username или email уже существует."
                "Однако username и email не соответствуют друг другу.",
            )

        if serializer_data["username"] == "me":
            raise serializers.ValidationError(
                "Невозможно создать пользователя с username `me`.",
            )
        return serializer_data


class UserTokenSerializer(serializers.Serializer):
    """User get token serializer."""

    username = serializers.SlugField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
    )
    confirmation_code = serializers.SlugField(required=True)

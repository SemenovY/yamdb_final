"""Users app views."""
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb import settings

from .models import User
from .permissions import IsAdmin
from .serializers import (
    UserCreationSerializer,
    UserSerializer,
    UserTokenSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request: HttpRequest) -> HttpResponse:
    """Sign up view.

    Args:
        request: HTTP request

    Returns:
        HTTP response
    """
    serializer = UserCreationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user_username = serializer.validated_data.get("username")
    user_email = serializer.validated_data.get("email")

    user, _ = User.objects.get_or_create(
        username=user_username,
        email=user_email,
    )
    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        subject="Код подтверждения",
        message=f"Ваш код подтверждения: {confirmation_code}",
        from_email=settings.FROM_EMAIL_DEFAULT,
        recipient_list=[user_email],
        fail_silently=False,
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_jwt_token(request: HttpRequest) -> HttpResponse:
    """Get jwt token view.

    Args:
        request: HTTP request

    Returns:
        HTTP response
    """
    serializer = UserTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    confirmation_code = serializer.validated_data.get("confirmation_code")
    user = get_object_or_404(User, username=username)

    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({"token": f"{token}"}, status=status.HTTP_200_OK)

    return Response(
        {"error": "Неверный код подтверждения."},
        status=status.HTTP_400_BAD_REQUEST,
    )


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = (IsAdmin | IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    http_method_names = ("get", "post", "patch", "delete")

    @action(
        methods=("patch", "get"),
        permission_classes=(IsAuthenticated,),
        detail=False,
        url_path="me",
        url_name="me",
    )
    def me(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Get self user data.

        Args:
            request: HTTP request
            args: Args
            kwargs: Kwargs

        Returns:
            HTTP response
        """
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True,
            )

            serializer.is_valid(raise_exception=True)
            serializer.validated_data["role"] = user.role
            serializer.save()
        return Response(serializer.data)

"""Custom mixins for creating and receiving subscriptions."""
from rest_framework import mixins, viewsets


class CreateListDestroy(  # noqa: WPS215
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Custom mixin, create an object and get a list."""

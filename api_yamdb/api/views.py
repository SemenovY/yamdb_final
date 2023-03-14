"""API views."""
from typing import Type

from django.db.models import Avg, QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitlesFilter
from .mixin import CreateListDestroy
from .permission import AdminOrReadOnly, AuthorAdminModeratorOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitlePostSerializer,
    TitleSerializer,
)


class ReviewViewSet(ModelViewSet):
    """View for Review."""

    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def get_queryset(self) -> QuerySet:
        """Get reviews queryset.

        Returns:
            Reviews queryset.
        """
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer: ReviewSerializer) -> None:
        """Create a new review.

        Args:
            serializer: Review serializer
        """
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(ModelViewSet):
    """View for Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def perform_create(self, serializer: CommentSerializer) -> None:
        """Create a new comment.

        Args:
            serializer: Comment serializer
        """
        review_id = self.kwargs.get("review_id")
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        review = get_object_or_404(Review, pk=review_id, title_id=title)
        serializer.save(review=review, author=self.request.user)


class CategoryViewSet(CreateListDestroy):
    """View for Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_fields = ("name", "slug")
    search_fields = ("name", "slug")


class GenreViewSet(CreateListDestroy):
    """View for Genre."""

    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    search_fields = ("name", "slug")
    filterset_fields = ("name", "slug")


class TitleViewSet(ModelViewSet):
    """View for Title."""

    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_class = TitlesFilter
    search_fields = ("name", "year", "genre__slug", "category__slug")

    def get_serializer_class(self) -> Type[ModelSerializer]:
        """Choose a serializer class for title.

        Returns:
            Chosen serializer class for title
        """
        if self.action in {"list", "retrieve"}:
            return TitleSerializer
        return TitlePostSerializer

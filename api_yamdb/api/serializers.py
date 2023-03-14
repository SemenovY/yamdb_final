"""Serializers for API."""
from datetime import datetime as dt
from typing import Optional

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category."""

    class Meta:
        """Fields for Category."""

        model = Category
        exclude = ("id",)


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre."""

    class Meta:
        """Fields for Genre."""

        model = Genre
        exclude = ("id",)


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        """Fields for Title."""

        model = Title
        fields = "__all__"

    def get_rating(self, title: Title) -> Optional[Review]:
        """Get title rating.

        Args:
            title: Title, the rating of which is given

        Returns:
            title rating
        """
        try:
            return title.reviews.all().aggregate(Avg("score"))["score__avg"]
        except TypeError:
            return None

    def validate_year(self, year: int) -> int:
        """Validate year value.

        Args:
            year: year value to be validated

        Returns:
            Validated year value

        Raises:
            ValidationError: if year value is not valid
        """
        current_year = dt.now().year
        if year > current_year:
            raise serializers.ValidationError("Проверьте год создания!")
        return year


class TitlePostSerializer(serializers.ModelSerializer):
    """Serializer for Post_Title."""

    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        """Fields for Title."""

        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        """Fields for Review."""

        model = Review
        exclude = ("title",)
        read_only_fields = ("author",)

    def validate(self, serializer_data: dict) -> dict:
        """Validate serializer data.

        Args:
            serializer_data: serializer data to be validated

        Returns:
            Serializer data

        Raises:
            ValidationError: if serializer data is not valid
        """
        request = self.context["request"]
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if (  # noqa: WPS337
            request.method == "POST"
            and Review.objects.filter(
                title=title,
                author=request.user,
            ).exists()
        ):
            raise serializers.ValidationError("Ошибка: отзыв уже создан")
        return serializer_data


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        """Fields for Comment."""

        model = Comment
        exclude = ("review",)
        read_only_fields = ("author",)

"""Custom filters."""
from django_filters import rest_framework as filters

from reviews.models import Title


class TitlesFilter(filters.FilterSet):
    """Fields titles filtered."""

    name = filters.CharFilter(field_name="name", lookup_expr="contains")
    category = filters.CharFilter(
        field_name="category__slug",
        lookup_expr="contains",
    )
    genre = filters.CharFilter(
        field_name="genre__slug",
        lookup_expr="contains",
    )

    class Meta:
        """Fields all."""

        model = Title
        fields = ("name", "genre", "category", "year")

"""Admin panel."""
from django.conf import settings
from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    """Admin panel for Category models."""

    list_display = ("pk", "name", "slug")
    list_editable = ("name",)
    search_fields = ("slug",)
    empty_value_display = settings.EMPTY_VALUE


class GenreAdmin(admin.ModelAdmin):
    """Admin panel for Genre models."""

    list_display = ("pk", "name", "slug")
    list_editable = ("name",)
    search_fields = ("slug",)
    empty_value_display = settings.EMPTY_VALUE


class TitleAdmin(admin.ModelAdmin):
    """Admin panel for Title models."""

    list_display = ("pk", "name", "year", "description", "category")
    list_editable = ("description",)
    search_fields = ("name",)
    list_filter = ("year",)
    empty_value_display = settings.EMPTY_VALUE


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Comment)
admin.site.register(Review)

"""Models for reviews."""
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from .validators import validate_year

User = get_user_model()

LONG_SLUG_LENGTH = 256
DESCRIPTION_LENGTH = 300
STRING_LENGTH = 20


class Category(models.Model):
    """Model for Category."""

    name = models.CharField(
        max_length=LONG_SLUG_LENGTH,
        unique=True,
        verbose_name="Категория",
        help_text="Укажите категорию",
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Поле slug для каждой категории.",
        help_text=(
            "Укажите уникальный адрес для страницы категории."
            "Используйте только "
            "латиницу, цифры, дефисы и знаки подчёркивания"
        ),
    )

    class Meta:
        """Meta for Category model."""

        ordering = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        """Format category name.

        Returns:
            Category name
        """
        return self.name[:STRING_LENGTH]


class Genre(models.Model):
    """Model for Genre."""

    name = models.CharField(
        max_length=LONG_SLUG_LENGTH,
        unique=True,
        verbose_name="Жанр",
        help_text="Укажите жанр произведения",
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Поле slug для каждого жанра.",
        help_text=(
            "Укажите уникальный адрес для страницы жанра."
            "Используйте только "
            "латиницу, цифры, дефисы и знаки подчёркивания"
        ),
    )

    class Meta:
        """Meta for Genre model."""

        ordering = ("name",)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        """Format genre name.

        Returns:
            Genre name
        """
        return self.name[:STRING_LENGTH]


class Title(models.Model):
    """Model for Title."""

    name = models.CharField(
        max_length=LONG_SLUG_LENGTH,
        verbose_name="Название произведения",
        help_text="Введите название произведения",
    )
    year = models.PositiveSmallIntegerField(
        validators=[validate_year],
        verbose_name="Год издания/публикации произведения",
        help_text="Укажите год выпуска",
        db_index=True,
    )
    description = models.CharField(
        max_length=DESCRIPTION_LENGTH,
        blank=True,
        verbose_name="Описание произведения",
        help_text="Введите описание произведения",
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
        help_text="Укажите жанр произведения",
        related_name="genres",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        help_text="Укажите категорию произведения",
        related_name="titles",
    )

    class Meta:
        """Title model meta."""

        ordering = ("category", "name")
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self) -> str:
        """Format title name.

        Returns:
            Title name
        """
        name = self.name[:STRING_LENGTH]
        return f"{name}, {str(self.year)}, {self.category}"

    def get_absolute_url(self) -> str:
        """Get the url to access admin panel.

        Returns:
            Title URL
        """
        return reverse("titles-list", args=[str(self.id)])


class Review(models.Model):
    """Model for Review."""

    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(
                10,
                message="Максимально допустимое значение - 10",
            ),
            MinValueValidator(
                1,
                message="Минимально допустимое значение - 1",
            ),
        ],
        verbose_name="Рейтинг",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата",
    )

    class Meta:
        """Meta for Review model."""

        verbose_name = "Отзыв"
        ordering = ("-pub_date",)
        unique_together = ("author", "title")


class Comment(models.Model):
    """Model for Comment."""

    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата",
    )

    class Meta:
        """Meta for Comment model."""

        verbose_name = "Комментарий"
        ordering = ("-pub_date",)

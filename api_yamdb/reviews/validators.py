"""Validators for reviews."""
from datetime import datetime as dt

from rest_framework import serializers


def validate_year(year: int) -> int:
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

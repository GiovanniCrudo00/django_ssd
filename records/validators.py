import pytest
from django.core.exceptions import ValidationError


def validate_humidity(value: int) -> None:
    if value < 0 or value > 100:
        raise ValidationError('Humidity must be between 0 and 100')


def validate_temperature(value: int) -> None:
    if value < -50 or value > 50:
        raise ValidationError('Temperature must be between -50 and 50')


def validate_wind(value: int) -> None:
    if value < 0 or value > 200:
        raise ValidationError('Wind must be between 0 and 200')

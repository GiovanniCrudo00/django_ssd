import pytest
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer


def test_dummy(db):
    assert True

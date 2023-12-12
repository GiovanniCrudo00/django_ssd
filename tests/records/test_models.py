import pytest
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer

from django.utils import timezone
from records.models import Record


@pytest.mark.parametrize('value', [
    -1,
    -10,
    101,
    150,
])
def test_record_humidity_lower_than_zero_or_higher_than_100_raises_exception(db, value):
    record = mixer.blend('records.Record', humidity=value)
    with pytest.raises(ValidationError) as err:
        record.full_clean()

    assert 'Humidity must be between 0 and 100' in '\n'.join(err.value.messages)


@pytest.mark.parametrize('value', [
    -51,
    51,
    -150,
    150
])
def test_record_temperature_exceeding_upperbound_and_lowerbound_raises_exception(db, value):
    record = mixer.blend('records.Record', temperature=value)
    with pytest.raises(ValidationError) as err:
        record.full_clean()

    assert 'Temperature must be between -50 and 50' in '\n'.join(err.value.messages)


@pytest.mark.parametrize('value', [
    -1,
    201,
    -150,
    350,
])
def test_record_wind_exceeding_upperbound_and_lowerbound_raises_exception(db, value):
    record = mixer.blend('records.Record', wind=value)
    with pytest.raises(ValidationError) as err:
        record.full_clean()

    assert 'Wind must be between 0 and 200' in '\n'.join(err.value.messages)


@pytest.mark.parametrize('value', [
    5,
    10,
    -1,
])
def test_record_wrong_condition_raises_exception(db, value):
    record = mixer.blend('records.Record', condition=value)
    with pytest.raises(ValidationError) as err:
        record.full_clean()

    assert 'is not a valid choice.' in '\n'.join(err.value.messages)  # This is the error message


@pytest.mark.parametrize('temperature, humidity, wind, date, condition', [
    (55, 15, 15, timezone.now(), '1'),
    (-55, 1, 400, timezone.now(), '4'),
    (10, 110, -40, timezone.now(), '3')
])
def test_wrong_record_creation_raises_exception(db, temperature, humidity, wind, date, condition):
    record = mixer.blend('records.Record', temperature=temperature, humidity=humidity, wind=wind,
                         date=date, condition=condition)
    with pytest.raises(ValidationError):
        record.full_clean()


def test_record_wrong_date_raises_exception(db):
    with pytest.raises(ValidationError) as e:
        mixer.blend('records.Record', date='a')

    assert 'value has an invalid format' in str(e.value)


# Correct date format: 2023-12-08T22:54:00Z
def test_correct_date_selection(db):
    today_datetime = timezone.now()

    record = mixer.blend('records.Record', date=today_datetime)
    record_instance = Record.objects.get(id=record.id)

    assert record_instance.date is not None
    assert record_instance.date == today_datetime


@pytest.mark.parametrize('temperature, humidity, wind, date, condition', [
    (15, 15, 15, timezone.now(), '1'),
    (-4, 1, 4, timezone.now(), '4'),
    (10, 90, 40, timezone.now(), '3')
])
def test_correct_record_creation(db, temperature, humidity, wind, date, condition):
    record = mixer.blend('records.Record', temperature=temperature, humidity=humidity, wind=wind,
                         date=date, condition=condition)
    record.full_clean()
    record_instance = Record.objects.get(id=record.id)
    assert record_instance.temperature == temperature
    assert record_instance.humidity == humidity
    assert record_instance.wind == wind
    assert record_instance.date == date
    assert record_instance.condition == condition

import re

import pytest
from records.models import Record
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from datetime import datetime
import json


@pytest.fixture()
def records(db):
    return [
        mixer.blend('records.Record'),
        mixer.blend('records.Record'),
        mixer.blend('records.Record'),
    ]


def get_client(user=None):
    res = APIClient()
    if user is not None:
        res.force_login(user)
    return res


def parse(response):
    response.render()
    content = response.content.decode()
    return json.loads(content)


def contains(response, key, value):
    obj = parse(response)
    if key not in obj:
        return False
    return value in obj[key]


def test_not_authenticated_users_get_forbidden_status_code():
    path = reverse('records-list')
    client = get_client()
    response = client.get(path)
    assert response.status_code == HTTP_403_FORBIDDEN
    assert contains(response, 'detail', 'Authentication credentials were not provided.')


def test_authenticated_common_user_gets_records_list(records):
    path = reverse('records-list')
    user = mixer.blend(get_user_model())
    group = Group.objects.create(name='common_user')
    user.groups.add(group)
    client = get_client(user)
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == len(records)


def test_authenticated_common_user_gets_single_record(records):
    path = reverse('records-detail', kwargs={'pk': records[0].pk})
    user = mixer.blend(get_user_model())
    group = Group.objects.create(name='common_user')
    user.groups.add(group)
    client = get_client(user)
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert obj['temperature'] == records[0].temperature
    assert obj['humidity'] == records[0].humidity
    assert obj['wind'] == records[0].wind
    assert obj['condition'] == records[0].condition
    # Now I need to cast the date in the response to a python datetime object
    date_obj = datetime.strptime(obj['date'], '%Y-%m-%dT%H:%M:%S%z')
    assert date_obj == records[0].date


def test_authenticated_record_editor_user_gets_multiple_records(records):
    path = reverse('records-list')
    user = mixer.blend(get_user_model())
    group = Group.objects.create(name='records_editors')
    user.groups.add(group)
    client = get_client(user)
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == len(records)


def test_authenticated_common_user_gets_forbidden_when_making_post(db):
    path = reverse('records-list')
    user = mixer.blend(get_user_model())
    group = Group.objects.create(name='common_user')
    user.groups.add(group)
    client = get_client(user)
    response = client.post(path, json.dumps({'mulinciana': 'mulinciana'}), content_type='application/json')
    assert response.status_code == HTTP_403_FORBIDDEN


def test_authenticated_superuser_gets_multiple_records(records, db):
    path = reverse('records-list')
    user = get_user_model().objects.create_superuser(
        username='superuser',
        password='super_pass',
        email='superuser@example.com'
    )
    client = get_client(user)
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == len(records)


def test_authenticated_user_with_non_existent_group_gives_forbidden(records):
    path = reverse('records-list')
    user = mixer.blend(get_user_model())
    group = Group.objects.create(name='fake-mulinciana-group')
    user.groups.add(group)
    client = get_client(user)
    response = client.get(path)
    assert response.status_code == HTTP_403_FORBIDDEN
    # See what it gives in the browsable API
    assert contains(response, 'detail', 'You do not have permission to perform this action.')


@pytest.fixture
def my_user(db):
    user = get_user_model().objects.create_user(
        username='mulinciana',
        password='mulinciana',
        email='mulinciana@example.com'
    )
    return user


def test_login_with_wrong_credentials_gives_error(db, my_user):
    path = "http://localhost:8000/api/v1/auth/login/"
    group = Group.objects.create(name='common_user')
    my_user.groups.add(group)
    client = get_client(my_user)
    login_data = json.dumps({
        "username": "wrong_username",
        "email": "",
        "password": "mulinciana"
    })
    response = client.post(path, data=login_data, content_type='application/json')
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert contains(response, 'non_field_errors', 'Unable to log in with provided credentials.')


def test_correct_login_and_logout_of_a_user(db, my_user):
    path = "http://localhost:8000/api/v1/auth/login/"

    group = Group.objects.create(name='common_user')
    my_user.groups.add(group)
    client = get_client(my_user)

    login_data = json.dumps({
        "username": "mulinciana",
        "email": "",
        "password": "mulinciana"
    })

    response = client.post(path, data=login_data, content_type='application/json')
    assert response.status_code == HTTP_200_OK

    # Here we need to check that the key is present, and it is long 40 chars
    assert 'key' in response.data
    assert re.match(r'[a-zA-Z0-9]{40}', response.data['key'])


def test_correct_logout_of_a_user(db):
    path = "http://localhost:8000/api/v1/auth/logout/"
    user = mixer.blend(get_user_model())
    group = Group.objects.create(name='common_user')
    user.groups.add(group)
    client = get_client(user)
    response = client.post(path, data=json.dumps({"": ""}), content_type='application/json')
    assert response.status_code == HTTP_200_OK
    assert contains(response, 'detail', 'Successfully logged out.')

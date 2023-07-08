import pytest
from django.contrib.auth.models import User

from accounts.models import Token


@pytest.fixture()
def in_active_user():
    return User.objects.create_user(username='user', password='password', is_active=False)


@pytest.fixture()
def token(in_active_user):
    return Token.objects.create(user=User.objects.first())


@pytest.fixture()
def active_user():
    return User.objects.create_user(username='user', password='password', is_active=True)

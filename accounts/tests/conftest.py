import pytest
from django.contrib.auth.models import User

from accounts.models import Token


@pytest.fixture()
def in_active_user():
    user = User.objects.create_user(username='user', password='password')
    user.is_active = False
    user.save()
    if user.is_active:
        user.last_name = 'dupa'
        user.save()
        return user
    return user


@pytest.fixture()
def token(in_active_user):
    return Token.objects.create(user=User.objects.first())

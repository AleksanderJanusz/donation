import pytest
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

from accounts.models import Token


@pytest.mark.django_db
def test_account_activation_valid(token):
    user = User.objects.first()
    assert not user.is_active
    client = Client()
    token = Token.objects.first()
    assert token.user == user
    url = reverse('activate', kwargs={'token': token.token})
    response = client.get(url)

    user = User.objects.first()
    assert user.is_active

    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_account_activation_in_valid(token):
    user = User.objects.first()
    assert not user.is_active
    client = Client()
    url = reverse('activate', kwargs={'token': 'invalid_token'})
    response = client.get(url)

    user = User.objects.first()
    assert not user.is_active

    assert response.status_code == 200
    assert type(response) == HttpResponse


@pytest.mark.django_db
def test_account_register_create_token():
    client = Client()
    url = reverse('register')
    data = {'first_name': 'first name',
            'last_name': 'last name',
            'email': 'email@wp.pl',
            'password1': 'password',
            'password2': 'password',
            }
    assert len(User.objects.all()) == 0
    assert len(Token.objects.all()) == 0
    response = client.post(url, data)

    assert response.status_code == 302
    assert len(User.objects.all()) == 1
    assert len(Token.objects.all()) == 1

    assert not User.objects.first().is_active


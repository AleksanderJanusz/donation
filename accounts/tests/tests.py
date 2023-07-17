import pytest
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from accounts.forms import RecoverPasswordForm
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
            'password1': 'Password!1',
            'password2': 'Password!1',
            }
    assert len(User.objects.all()) == 0
    assert len(Token.objects.all()) == 0
    response = client.post(url, data)

    assert response.status_code == 302
    assert len(User.objects.all()) == 1
    assert len(Token.objects.all()) == 1

    assert not User.objects.first().is_active


@pytest.mark.django_db
def test_password_recovery_token_valid(active_user):
    client = Client()
    url = reverse('recover_password_token')
    user = User.objects.first()
    data = {'email': user.email}

    assert len(Token.objects.all()) == 0
    response = client.post(url, data)

    assert response.status_code == 200
    assert len(Token.objects.all()) == 1
    assert type(response) == HttpResponse


@pytest.mark.django_db
def test_password_recovery_token_in_valid(active_user):
    client = Client()
    url = reverse('recover_password_token')
    data = {'email': 'in_valid_email'}

    assert len(Token.objects.all()) == 0
    response = client.post(url, data)

    assert response.status_code == 200
    assert len(Token.objects.all()) == 0
    assert response.context['error']


@pytest.mark.django_db
def test_password_recovery_get_in_valid(token):
    client = Client()
    url = reverse('password_recovery', kwargs={'token': 'token'})
    response = client.get(url)

    assert response.status_code == 200
    assert not response.context


@pytest.mark.django_db
def test_password_recovery_get_valid(token):
    client = Client()
    token = Token.objects.first()
    url = reverse('password_recovery', kwargs={'token': token.token})
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.context['form'], RecoverPasswordForm)


@pytest.mark.django_db
def test_password_recovery_post_valid(token):
    client = Client()
    token = Token.objects.first()
    assert len(Token.objects.all()) == 1
    url = reverse('password_recovery', kwargs={'token': token.token})
    data = {'password1': 'Password!1',
            'password2': 'Password!1'}
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
    assert len(Token.objects.all()) == 0


@pytest.mark.django_db
def test_password_recovery_post_in_valid(token):
    client = Client()
    token = Token.objects.first()
    assert len(Token.objects.all()) == 1
    url = reverse('password_recovery', kwargs={'token': token.token})
    data = {'password1': 'Password!1',
            'password2': 'Password!2'}
    response = client.post(url, data)

    assert response.status_code == 200
    assert isinstance(response.context['form'], RecoverPasswordForm)
    assert len(Token.objects.all()) == 1


@pytest.mark.django_db
def test_login_valid(active_user):
    client = Client()
    url = reverse('login')
    data = {'username': 'user',
            'password': 'password'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('index'))


@pytest.mark.django_db
def test_login_in_valid(active_user):
    client = Client()
    url = reverse('login')
    data = {'username': 'user',
            'password': 'pass'}
    response = client.post(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_in_valid_redirect(active_user):
    client = Client()
    url = reverse('login')
    data = {'username': 'wrong user',
            'password': 'pass'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('register'))

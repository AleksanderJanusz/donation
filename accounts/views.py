from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mass_mail, send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView
from django.urls import reverse

from accounts.forms import AddUserForm, LoginForm, EditUserForm, RecoverPasswordForm
from accounts.models import Token


def send_token_email(token, request, email, message, url_name):
    current_site = get_current_site(request)
    activation_url = reverse(url_name, kwargs={'token': token.token})
    activation_link = f'http://{current_site.domain}{activation_url}'
    subject = 'GiveCare'
    message = f'{message}{activation_link}'
    email_from = 'portfolio.givecare@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        url_to_go = request.GET.get('next')
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            if user is not None:
                login(request, user)
            if url_to_go:
                return redirect(url_to_go)
            return redirect('index')
        is_user = User.objects.filter(username=form.cleaned_data['username'])
        if not is_user:
            return redirect('register')
        return render(request, 'accounts/login.html', {'form': form})


class Register(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.username = form.cleaned_data['email']
            user.is_active = False
            user.save()
            token = Token.objects.create(user=user)
            message = 'Kliknij w link aby aktywować konto: '
            url_name = 'activate'
            send_token_email(token, request, user.email, message, url_name)
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})


class Logout(View):

    def get(self, request):
        url_to_go = request.GET.get('next')
        logout(request)
        if url_to_go:
            return redirect(url_to_go)
        return redirect('index')


class Edit(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/edit.html')

    def post(self, request):
        user = authenticate(username=request.user.username, password=request.POST.get('password'))
        form = EditUserForm(request.POST, instance=user)
        error = False
        if form.is_valid():
            error = True
        if user is not None and error:
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return redirect('edit')

        return render(request, 'accounts/edit.html', {'error': error, 'form': form.errors})


class ChangePassword(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/change_password.html')

    def post(self, request):
        user = authenticate(username=request.user.username, password=request.POST.get('password_old'))
        form = RecoverPasswordForm(request.POST)
        error = False
        if form.is_valid() and user:
            user.set_password(form.cleaned_data['password1'])
            user.save()
        if not user:
            error = 'stare hasło nieprawidłowe'
        return render(request, 'accounts/change_password.html', {'error': error, 'form': form})


class Activate(View):
    def get(self, request, token):
        try:
            activate_token = Token.objects.get(token=token)
        except ObjectDoesNotExist:
            return HttpResponse('Link jest nie aktywny, skontaktuj się z nami w celu rozwiązania problemu')
        if activate_token.active:
            user = User.objects.get(pk=activate_token.user_id)
            user.is_active = True
            user.save()
            activate_token.delete()
            return redirect('login')
        return HttpResponse('Link jest nie aktywny, skontaktuj się z nami w celu rozwiązania problemu')


class PasswordRecoveryToken(View):
    def get(self, request):
        return render(request, 'accounts/recovery/generate_token.html')

    def post(self, request):
        email = request.POST.get('email')
        user = User.objects.filter(email=email)
        if user:
            token = Token.objects.create(user=user[0])
            message = 'Kliknij w link aby zmienić hasło: '
            url_name = 'password_recovery'
            send_token_email(token, request, email, message, url_name)
            return HttpResponse('Email z linkiem został wysłany')
        return render(request, 'accounts/recovery/generate_token.html', {'error': True})


class PasswordRecovery(View):
    def get(self, request, token):
        form = RecoverPasswordForm()
        token = Token.objects.filter(token=token)
        if not token or not token[0].active:
            return HttpResponse('Link jest nie aktywny, skontaktuj się z nami w celu rozwiązania problemu')
        return render(request, 'accounts/recovery/change_password_from_token.html', {'form': form})

    def post(self, request, token):
        form = RecoverPasswordForm(request.POST)
        token = Token.objects.get(token=token)

        if not token.active:
            return HttpResponse('Coś poszło nie tak, skontaktuj się z nami w celu rozwiązania problemu')
        if form.is_valid():
            user = User.objects.get(pk=token.user_id)
            user.set_password(form.cleaned_data['password1'])
            token.delete()
            user.save()
            return redirect('login')
        return render(request, 'accounts/recovery/change_password_from_token.html', {'form': form})

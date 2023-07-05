from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView
from django.urls import reverse

from accounts.forms import AddUserForm, LoginForm, EditUserForm


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
            user.save()
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
        form = EditUserForm(request.POST)
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
        password1 = request.POST.get('password_new1')
        password2 = request.POST.get('password_new2')
        error = False
        if not password1:
            error = 'hasło nie może być puste'
        if password1 != password2:
            error = 'nowe hasła się różnią'
        if user is not None and not error:
            user.set_password(password1)
            user.save()
            return redirect('edit')
        if not error:
            error = 'stare hasło nieprawidłowe'
        return render(request, 'accounts/change_password.html', {'error': error})

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import AddUserForm, LoginForm


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            if user is not None:
                login(request, user)
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
        logout(request)
        return redirect('index')

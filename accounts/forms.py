from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import redirect


class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='')
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}), label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}), label='')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise ValidationError('Hasła nie są identyczne')
        return cleaned_data

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='')

    def clean(self):
        cleaned_data = super().clean()
        user = authenticate(**cleaned_data)
        if user is None:
            raise ValidationError('Nie poprawne hasło')
        cleaned_data['user'] = user
        return cleaned_data

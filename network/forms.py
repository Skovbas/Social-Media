from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255, help_text="Required. Add a valid email address.")

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
            raise forms.ValidationError(f'Email {email} is already in use.')
        except Account.DoesNotExist:
            return email

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.get(username=username)
            raise forms.ValidationError(f'Email {username} is already in use.')
        except Account.DoesNotExist:
            return username

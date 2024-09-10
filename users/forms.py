from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ['email']

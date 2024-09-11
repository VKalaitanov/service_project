from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        labels = {
            'email': "E-mail"
        }
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Enter Your Email Address'}),
        }


class RegisterUserForm(UserCreationForm):
    email = forms.CharField(label="E-mail",
                            widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Reply password",
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']

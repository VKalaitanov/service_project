from django.conf import settings
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Login'}

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Register"}
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.send_email(user)
        return super().form_valid(form)

    def send_email(self, user):
        subject = 'Confirm your account'
        message = f"""Hi Thank you for registering.
         Please confirm your email address to complete the registration.
         \n\nBest regards,\nYour Website"""
        from_email = settings.DEFAULT_FROM_EMAIL
        print(user.username)
        print(user.email)
        recipient_list = [user.email]
        print('отправляем')
        send_mail(subject, message, from_email, recipient_list)
        print("отправили")

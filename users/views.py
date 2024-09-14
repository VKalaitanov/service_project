from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView

from .forms import LoginUserForm, RegisterUserForm
from .utils import account_activation_token


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
    success_url = reverse_lazy('users:email_confirmation_sent')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Пользователь неактивен до подтверждения email
        user.save()

        current_site = get_current_site(self.request).domain
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        activation_url = reverse_lazy(
            'users:confirm_email',
            kwargs={'uidb64': uid, 'token': token}
        )
        self.send_message_by_email(current_site=current_site,
                                   activation_url=activation_url,
                                   user=user)
        return super().form_valid(form)

    def send_message_by_email(self, current_site, activation_url, user):
        recipient_list = [user.email]
        subject = 'Подтвердите свой электронный адрес'
        message = (
            f'Активация email на сайте {current_site}, если вы не регистрировались \n'
            f'на нашем сайте, игнорируйте это сообщение. \n'
            f'Иначе пожалуйста, перейдите по следующей ссылке, чтобы подтвердить \n'
            f'свой адрес электронной почты: https://{current_site}{activation_url}'
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, recipient_list)


class UserConfirmEmailView(View):

    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'
    extra_context = {'title': 'Activation email sent'}


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'
    extra_context = {'title': 'Your email address has been activated'}


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'
    extra_context = {'title': 'Invalid link'}

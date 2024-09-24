from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView

from .forms import LoginUserForm, RegisterUserForm
from .utils import account_activation_token, send_verification_email
from orders.forms import DynamicOrderForm
from orders.models import Order
from service.models import Service
from .service import ControlBalance

@csrf_exempt
def resend_verification_email(request):
    if request.method == "POST":
        user_email = request.session.get('user_email')

        if not user_email:
            return JsonResponse({'error': 'No email in session'}, status=400)

        try:
            user = get_user_model().objects.get(email=user_email)
        except get_user_model().DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        if not user.is_active:
            # Отправляем email для неактивного пользователя
            send_verification_email(request, user)
            return JsonResponse({'message': 'Verification email resent successfully!'})

        return JsonResponse({'error': 'Account is already active.'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Login'}

    def get_success_url(self):
        return reverse_lazy('users:profile')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Register"}
    success_url = reverse_lazy('users:email_confirmation_sent')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        self.request.session['user_email'] = user.email
        send_verification_email(self.request, user)
        return super().form_valid(form)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем email из сессии
        user_email = self.request.session.get('user_email')
        context['user_email'] = user_email
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'
    extra_context = {'title': 'Your email address has been activated'}


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'
    extra_context = {'title': 'Invalid link'}


class CustomPasswordResetView(PasswordResetView):
    """Класс для старта сброса пароля"""
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = email_template_name
    success_url = reverse_lazy('users:password_reset_done')
    extra_email_context = {"image_url": 'https://dogehype.com/public/icon.png'}
    subject_template_name = 'users/password_reset_subject.txt'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


class ProfileUser(LoginRequiredMixin, TemplateView, ControlBalance):
    model = get_user_model()
    template_name = 'users/profile.html'
    extra_context = {
        'title': "Profile user",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        services = Service.objects.all().prefetch_related('options')  # Получаем все доступные сервисы
        forms = []

        for service in services:
            service_options = service.options.all()
            for service_option in service_options:
                form = DynamicOrderForm(service_option=service_option)
                forms.append((service, service_option, form))

        orders = Order.objects.filter(user=self.request.user)

        context['forms'] = forms
        context['services'] = services
        context['orders'] = orders

        return context

    def post(self, request, *args, **kwargs):
        services = Service.objects.all()
        forms = []

        if request.method == 'POST':
            for service in services:
                service_options = service.options.all()
                for service_option in service_options:
                    form = DynamicOrderForm(request.POST, service_option=service_option)
                    forms.append((service, service_option, form))

                    if form.is_valid():
                        custom_data = {}
                        for field_name in service_option.required_fields.keys():
                            custom_data[field_name] = form.cleaned_data[field_name]

                        period = form.cleaned_data.get('period') if service_option.has_period else None
                        self.place_an_order(
                            request=request, service=service,
                            service_option=service_option, custom_data=custom_data,
                            quantity=form.cleaned_data['quantity'], period=period
                        )

            # После успешного создания всех заказов перенаправляем пользователя
            return redirect(self.get_success_url())

        # Если форма не валидна или это не POST-запрос, рендерим страницу заново
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

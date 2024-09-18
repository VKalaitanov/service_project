from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [

    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # ------- Регистрация пользователя ------- #
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('confirm-email/<str:uidb64>/<str:token>/', views.UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmation-sent/', views.EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('email-confirmed/', views.EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', views.EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),

    # ------- Восстановление пароля ------- #
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

from django.urls import path

from . import views
from .views import load_services

app_name = 'service'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('load_services/', load_services, name='load_services'),
]

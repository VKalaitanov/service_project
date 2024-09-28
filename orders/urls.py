from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('create/', views.OrderView.as_view())
]

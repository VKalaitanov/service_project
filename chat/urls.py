# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('all/', views.GetAllViews.as_view()),
    path("<int:room_name>/", views.index, name="index"),
]

from django.urls import path

from . import views

urlpatterns = [
    path('all/', views.GetAllViews.as_view()),
    path("<int:id_room>/", views.index, name="index"),
]

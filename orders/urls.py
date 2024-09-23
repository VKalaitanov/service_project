from django.urls import path
from . import views

urlpatterns = [
    path('order/<int:service_option_id>/', views.create_order, name='create_order'),
    # path('order/success/<int:order_id>/', views.order_success, name='order_success'),  # Страница успеха
]

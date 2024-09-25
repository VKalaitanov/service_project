from django.contrib.auth import get_user_model
from orders.models import Order


class ControlBalance:

    def place_an_order(self, request, service, service_option, custom_data, quantity, period):
        user = get_user_model().objects.get(email=request.user)
        total_price = service_option.price_per_unit * quantity
        if user.balance < total_price:
            return None
        Order.objects.create(
            user=request.user,
            service=service,
            service_option=service_option,
            custom_data=custom_data,
            quantity=quantity,
            total_price=total_price,
            status='pending',
            period=period
        )

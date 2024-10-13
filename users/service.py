from orders.models import Order


class ControlBalance:

    def place_an_order(self, user, service, service_option, custom_data, quantity, period, comment):
        discounted_price = service_option.get_discounted_price(user=user)  # Передаем пользователя
        total_price = discounted_price * quantity

        if user.balance < total_price:
            raise ValueError("У вас недостаточно средств")

        user.balance -= total_price
        user.save()

        Order.objects.create(
            user=user,
            service=service,
            service_option=service_option,
            custom_data=custom_data,
            quantity=quantity,
            total_price=total_price,
            status='pending',
            period=period,
            comment=comment,
        )
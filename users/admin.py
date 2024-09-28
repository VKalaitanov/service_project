from typing import Union

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import CustomerUser


@admin.register(CustomerUser)
class AdminCustomerUser(admin.ModelAdmin):
    fields = ['email', 'balance', 'order_user', 'sum_order', 'link_for_orders']
    save_on_top = True
    readonly_fields = ['email', 'order_user', 'sum_order', 'link_for_orders']
    list_display = ['email', 'balance', 'order_user']
    search_fields = ['email']

    @admin.display(description="Количество активных заказов")
    def order_user(self, obj) -> Union[str, int]:
        orders = obj.orders.filter(status='pending')
        if orders:
            return len(orders)
        return "Заказов нет"

    @admin.display(description="Заказы на общую сумму")
    def sum_order(self, obj):
        orders = obj.orders.filter(status='pending')
        if orders:
            return sum([order.total_price for order in orders])
        return 0

    @admin.display(description='ID заказов')
    def link_for_orders(self, obj):
        orders = obj.orders.filter(status='pending')
        if orders:
            links = [
                f"<a href='http://127.0.0.1:8000/admin/orders/order/{order.pk}/change/'>{order.pk}</a>"
                for order in orders
            ]
            return mark_safe(", ".join(links))
        return "Нет заказов"

    def has_add_permission(self, request):
        return False

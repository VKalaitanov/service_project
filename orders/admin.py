from django.contrib import admin
from .models import OrderUser


@admin.register(OrderUser)
class OrderAdmin(admin.ModelAdmin):
    fields = ['user', 'total_price', 'time_create', 'status']
    list_display = ['title_order']
    readonly_fields = ['user', 'total_price', 'time_create']

    @admin.display(description='Заказ')
    def title_order(self, obj):
        return str(obj)



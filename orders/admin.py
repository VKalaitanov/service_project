from django.contrib import admin
from .forms import ServiceOptionAdminForm

from .models import Service, ServiceOption, Order, ReplenishmentBalance

admin.site.register(Service)


class ServiceOptionAdmin(admin.ModelAdmin):
    form = ServiceOptionAdminForm


admin.site.register(ServiceOption, ServiceOptionAdmin)


@admin.register(ReplenishmentBalance)
class ReplenishmentBalanceAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'balance_for_replenishment',
        'email',
        'status'
    ]

    readonly_fields = [
        'user',
        'balance_for_replenishment',
        'email'
    ]

    list_display = [
        'user',
        'balance_for_replenishment'
    ]

    list_display_links = list_display

    search_fields = ['user']

    def has_add_permission(self, request):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = [
        'service',
        'service_option',
        'user',
        'custom_data',
        'quantity',
        'total_price',
        'status',
        'period',
        'created_at',
        'completed',
        'notes'
    ]

    readonly_fields = [
        'service',
        'service_option',
        'user',
        'quantity',
        'created_at',
        'total_price',
        'completed'
    ]

    list_display = [
        'service',
        'service_option',
        'user',
        'total_price'
    ]

    list_display_links = list_display
    search_fields = ['user']

    def has_add_permission(self, request):
        return False

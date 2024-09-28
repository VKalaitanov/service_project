from django.contrib import admin
from .models import Service, ServiceOption, Order, ReplenishmentBalance

admin.site.register(Service)
admin.site.register(ServiceOption)
admin.site.register(Order)
admin.site.register(ReplenishmentBalance)

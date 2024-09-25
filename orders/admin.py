from django.contrib import admin
from .models import Service, ServiceOption, Order

admin.site.register(Service)
admin.site.register(ServiceOption)
admin.site.register(Order)
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):

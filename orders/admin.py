from django.contrib import admin
from .models import Order

admin.site.register(Order)
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):

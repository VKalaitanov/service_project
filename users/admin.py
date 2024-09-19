from django.contrib import admin
from .models import CustomerUser


@admin.register(CustomerUser)
class AdminCustomerUser(admin.ModelAdmin):
    fields = ['email', 'balance']
    save_on_top = True
    readonly_fields = ['email']
    list_display = ['email', 'balance']
    search_fields = ['email']

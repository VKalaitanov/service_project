from django.contrib import admin

from .models import Service, Category, ServiceDetail

class ServiceDetailInline(admin.TabularInline):
    model = ServiceDetail
    extra = 3  # Количество пустых полей для добавления


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # fields = (
    #     'name', 'slug', 'image', 'description', 'price',
    #     'discount_price', 'available', 'category'
    # )
    inlines = [ServiceDetailInline]
    list_display = ('name', 'description', 'price', 'category')
    list_filter = ('name', 'category', 'price')
    # readonly_fields = ('slug', )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

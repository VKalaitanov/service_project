from django.db import models
from users.models import CustomerUser
from service.models import Service, ServiceOption
from djmoney.models.fields import MoneyField


class Order(models.Model):
    class ChoicesStatus(models.Choices):
        PENDING = 'pending'
        COMPLETED = 'completed'

    class PeriodChoices(models.Choices):
        HOUR = 'Hour'
        DAY = 'Day'
        WEEK = 'Week'
        MONTH = 'Month'

    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Сервис")

    service_option = models.ForeignKey(ServiceOption, on_delete=models.CASCADE, verbose_name='Опции')

    user = models.ForeignKey(CustomerUser, related_name="orders", on_delete=models.CASCADE, verbose_name='Пользователь')  # Заказчик

    custom_data = models.JSONField(
        verbose_name='Поля')  # Динамическое поле для хранения данных (username, ссылка и т.д.)

    quantity = models.IntegerField(verbose_name='Количество')  # Количество (лайков, подписчиков и т.д.)

    total_price = MoneyField(max_digits=10, decimal_places=2,
                             verbose_name='Цена', default=0,
                             default_currency="USD")

    status = models.CharField(max_length=50, choices=ChoicesStatus.choices, default=ChoicesStatus.PENDING,
                              verbose_name='Статус')

    period = models.CharField(max_length=50, blank=True, null=True, choices=PeriodChoices.choices,
                              default=PeriodChoices.HOUR,
                              verbose_name='Период')  # Период в днях, может быть пустым

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def calculate_total_price(self):
        self.total_price = self.service_option.price_per_unit * self.quantity
        self.save()

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

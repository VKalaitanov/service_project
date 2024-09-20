from django.db import models
from djmoney.models.fields import MoneyField
from users.models import CustomerUser


class OrderUser(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='orders',
                             verbose_name="E-mail пользователя")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    total_price = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11,
                             verbose_name="Сумма заказа")
    status = models.BooleanField(default=True, verbose_name="Статус заказа")

    def __str__(self):
        return f"ID: {self.pk}, User: {self.user.email} | Price - {self.total_price}"  # type: ignore

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

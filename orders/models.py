from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField
from users.models import CustomerUser


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название сервиса")  # Название сервиса (YouTube, VK и т.д.)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сервис"
        verbose_name_plural = "Сервисы"


class ServiceOption(models.Model):
    service = models.ForeignKey(Service, related_name='options', on_delete=models.CASCADE,
                                verbose_name="Название сервиса")

    name = models.CharField(max_length=255, verbose_name="Категория")  # Например, "Followers" или "Likes"

    price_per_unit = MoneyField(max_digits=10, decimal_places=2,
                                verbose_name='Цена', default=0,
                                default_currency="USD")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Скидка (%)")

    required_fields = models.JSONField(default=dict, verbose_name="Поля для заполнения")  # Динамические поля для услуги
    has_period = models.BooleanField(default=False,
                                     verbose_name="Добавить период", )
    #  Указывает, нужно ли поле "period" для этой услуги
    created_at = models.DateTimeField(auto_now_add=True)

    def get_discounted_price(self):
        """Возвращает цену с учётом скидки"""
        if self.discount_percentage > 0:
            return self.price_per_unit * (1 - self.discount_percentage / 100)
        return self.price_per_unit

    def __str__(self):
        return f"{self.name} for {self.service.name}"

    class Meta:
        verbose_name = "Настройки сервиса"
        verbose_name_plural = "Настройки сервисов"


class Order(models.Model):
    class ChoicesStatus(models.Choices):
        PENDING = 'pending'
        RUNNING = 'running'
        COMPLETED = 'completed'

    class PeriodChoices(models.Choices):
        HOUR = 'Hour'
        DAY = 'Day'
        WEEK = 'Week'
        MONTH = 'Month'

    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Сервис")

    service_option = models.ForeignKey(ServiceOption, on_delete=models.CASCADE, verbose_name='Опции')

    user = models.ForeignKey(CustomerUser, related_name="orders", on_delete=models.CASCADE,
                             verbose_name='Пользователь')  # Заказчик

    custom_data = models.JSONField(  # Динамическое поле для хранения данных (username, ссылка и т.д.)
        verbose_name='Поля, пример: {"username": "username"}')

    quantity = models.IntegerField(
        verbose_name='Количество')  # Количество (лайков, подписчиков и т.д.)

    total_price = MoneyField(max_digits=10, decimal_places=2,
                             verbose_name='Общая сумма заказа', default=0,
                             default_currency="USD")

    status = models.CharField(max_length=50, choices=ChoicesStatus.choices, default=ChoicesStatus.PENDING,
                              verbose_name='Статус')

    period = models.CharField(max_length=50, blank=True, null=True, choices=PeriodChoices.choices,
                              default=PeriodChoices.HOUR,
                              verbose_name='Период')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    notes = models.TextField(blank=True, verbose_name="Примечания")

    completed = models.DateTimeField(null=True, blank=True, verbose_name='Время завершения')
    admin_completed_order = models.CharField(max_length=255,
                                             blank=True, null=True,
                                             verbose_name='Завершено администратором')

    def save(self, *args, **kwargs):
        if self.status == self.ChoicesStatus.COMPLETED.value and self.completed is None:
            self.completed = timezone.now()
        super().save(*args, **kwargs)  # Сохраняем объект перед изменением admin_completed_order

    def calculate_total_price(self):
        """Рассчитывает общую стоимость с учётом скидки"""
        discounted_price = self.service_option.get_discounted_price()  # Получаем цену с учётом скидки
        self.total_price = discounted_price * self.quantity
        self.save()

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ('-created_at',)


class ReplenishmentBalance(models.Model):
    class ChoicesStatus(models.Choices):
        PENDING = 'pending'
        RUNNING = 'running'
        COMPLETED = 'completed'

    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='replenishment')
    balance_for_replenishment = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11,
                                           verbose_name="Сумма пополнения")
    email = models.EmailField(max_length=255, verbose_name="E-mail для связи")
    status = models.CharField(max_length=50, choices=ChoicesStatus.choices, default=ChoicesStatus.PENDING,
                              verbose_name="Статус заказа")

    def __str__(self):
        return f"User - {self.email}, balance - {self.balance_for_replenishment}"

    class Meta:
        verbose_name = 'Заказ на пополнение баланса'
        verbose_name_plural = 'Заказы на пополнение баланса'

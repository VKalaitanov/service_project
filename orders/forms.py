from django import forms
from django.core.exceptions import ValidationError
from djmoney.money import Money

from .models import ReplenishmentBalance, ServiceOption


class DynamicOrderForm(forms.Form):
    quantity = forms.IntegerField(label="Количество", min_value=1)
    comment = forms.CharField(label='Комментарий', max_length=255, required=False)

    PERIOD_CHOICES = [
        ('Hour', 'Hour'),
        ('Day', 'Day'),
        ('Week', 'Week'),
        ('Month', 'Month'),
    ]

    def __init__(self, *args, **kwargs):
        self.service_option = kwargs.pop('service_option', None)
        self.user = kwargs.pop('user', None)
        super(DynamicOrderForm, self).__init__(*args, **kwargs)

        # Добавляем динамические поля из required_fields
        if self.service_option and self.service_option.required_fields:
            for field_name, label in self.service_option.required_fields.items():
                self.fields[field_name] = forms.CharField(label=label, required=True)

        # Если услуга требует поле "period", добавляем его как выбор
        if self.service_option and self.service_option.has_period:
            self.fields['period'] = forms.ChoiceField(
                label="Период",
                required=False,
                choices=self.PERIOD_CHOICES
            )

        # Определяем порядок полей: динамические поля -> period -> quantity
        field_order = list(self.fields.keys() - ['period', 'quantity', 'comment'])  # Все динамические поля
        if 'period' in self.fields:
            field_order.append('period')  # Добавляем period перед quantity, если поле есть
        field_order.append('quantity')
        field_order.append('comment')

        # Применяем порядок
        self.order_fields(field_order)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        total_price = self.service_option.price_per_unit * quantity
        if self.user.balance < total_price:
            raise ValidationError("У вас недостаточно средств")
        return quantity


class CreateOrderForm(forms.ModelForm):
    balance_for_replenishment = forms.DecimalField(
        label='Balance for replenishment in dollars',
        max_digits=11,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter amount in dollars'})
    )

    class Meta:
        model = ReplenishmentBalance
        fields = ["email", "balance_for_replenishment"]
        labels = {
            'email': "E-mail to contact you",
            'balance_for_replenishment': 'Balance for replenishment in dollars'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter amount in dollars'})
        }


class ServiceOptionAdminForm(forms.ModelForm):
    class Meta:
        model = ServiceOption
        fields = '__all__'

    def clean_price_per_unit(self):
        price = self.cleaned_data.get('price_per_unit')
        if price <= Money(0, currency="USD"):
            raise ValidationError('Цена за штуку не должна быть меньше 0 или ровна 0')
        return price

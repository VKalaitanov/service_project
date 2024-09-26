from django import forms
from django.core.exceptions import ValidationError


class DynamicOrderForm(forms.Form):
    quantity = forms.IntegerField(label="Количество", min_value=1)

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
        field_order = list(self.fields.keys() - ['period', 'quantity'])  # Все динамические поля
        if 'period' in self.fields:
            field_order.append('period')  # Добавляем period перед quantity, если поле есть
        field_order.append('quantity')  # Добавляем quantity в конец

        # Применяем порядок
        self.order_fields(field_order)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        total_price = self.service_option.price_per_unit * quantity
        if self.user.balance < total_price:
            raise ValidationError("У вас недостаточно средств")
        return quantity

from django import forms


class DynamicOrderForm(forms.Form):
    quantity = forms.IntegerField(label="Количество", min_value=1)

    PERIOD_CHOICES = [
        ('Hour', 'Hour'),
        ('Day', 'Day'),
        ('Week', 'Week'),
        ('Month', 'Month'),
    ]

    def __init__(self, *args, **kwargs):
        service_option = kwargs.pop('service_option', None)
        super(DynamicOrderForm, self).__init__(*args, **kwargs)

        # Добавляем динамические поля из required_fields
        if service_option and service_option.required_fields:
            for field_name, label in service_option.required_fields.items():
                if field_name == 'link':
                    self.fields[field_name] = forms.URLField(label=label, required=True)
                elif field_name == 'int':
                    self.fields[field_name] = forms.IntegerField(label=label, required=True)
                self.fields[field_name] = forms.CharField(label=label, required=True)

        # Если услуга требует поле "period", добавляем его как выбор
        if service_option and service_option.has_period:
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

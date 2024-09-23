from django import forms


class DynamicOrderForm(forms.Form):
    quantity = forms.IntegerField(label="Количество", min_value=1)

    # Варианты выбора для периода
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
                self.fields[field_name] = forms.CharField(label=label, required=True)

        # Если услуга требует поле "period", добавляем его как выбор
        if service_option and service_option.has_period:
            self.fields['period'] = forms.ChoiceField(
                label="Период",
                required=False,
                choices=self.PERIOD_CHOICES
            )

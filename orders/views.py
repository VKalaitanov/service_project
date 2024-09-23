from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from service.models import ServiceOption  # type: ignore
from .forms import DynamicOrderForm
from django.contrib.auth.decorators import login_required


@login_required
def create_order(request, service_option_id):
    service_option = get_object_or_404(ServiceOption, id=service_option_id)

    if request.method == 'POST':
        form = DynamicOrderForm(request.POST, service_option=service_option)
        if form.is_valid():
            # Собираем данные для создания заказа
            custom_data = {}
            for field_name in service_option.required_fields.keys():
                custom_data[field_name] = form.cleaned_data[field_name]

            # Если есть поле "period", добавляем его в данные заказа
            period = form.cleaned_data.get('period') if service_option.has_period else None

            # Создаем заказ
            Order.objects.create(  # type: ignore
                user=request.user,
                service=service_option.service,
                service_option=service_option,
                custom_data=custom_data,  # Данные из динамических полей
                quantity=form.cleaned_data['quantity'],  # Количество
                total_price=service_option.price_per_unit * form.cleaned_data['quantity'],  # Итоговая цена
                status='pending',  # Статус заказа
                period=period  # Если был выбран период, он сохраняется
            )
            return redirect("users:profile")
    else:
        form = DynamicOrderForm(service_option=service_option)

    return render(request, 'orders/create_order.html', {'form': form, 'service_option': service_option})

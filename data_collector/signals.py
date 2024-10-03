from django.db import transaction
from django.db.models import F
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from orders.models import Order  # type: ignore
from .models import DailyOrderAnalytics


@receiver(post_save, sender=Order)
def add_new_order_to_analytics(sender, instance, created, **kwargs):
    with transaction.atomic():
        date_collect, created_date_collect = DailyOrderAnalytics.objects.get_or_create(date=timezone.now().date())

        if created:
            date_collect.total_orders = F('total_orders') + 1
            date_collect.total_revenue = F('total_revenue') + instance.total_price
            date_collect.save(update_fields=['total_orders', 'total_revenue'])

        elif instance.status == 'completed':
            date_collect.completed_orders = F('completed_orders') + 1

            info_completed_orders = date_collect.info_completed_orders
            info_completed_orders['service'].append(instance.service.name)
            info_completed_orders['option'].append(instance.service_option.name)
            info_completed_orders['user'].append(instance.user.email)
            info_completed_orders['completed'].append(instance.completed.strftime('%Y-%m-%d %H:%M:%S'))

            date_collect.info_completed_orders = info_completed_orders
            date_collect.save(update_fields=['completed_orders', 'info_completed_orders'])

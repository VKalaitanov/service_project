# Generated by Django 5.1.1 on 2024-10-09 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_alter_order_period_alter_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='period',
            field=models.CharField(blank=True, choices=[('Hour', 'Hour'), ('Day', 'Day'), ('Week', 'Week'), ('Month', 'Month')], default='Hour', max_length=50, null=True, verbose_name='Период'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('running', 'Running'), ('completed', 'Completed')], default='pending', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='replenishmentbalance',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('running', 'Running'), ('completed', 'Completed')], default='pending', max_length=50, verbose_name='Статус заказа'),
        ),
    ]

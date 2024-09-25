# Generated by Django 5.1.1 on 2024-09-25 12:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='order',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.service', verbose_name='Сервис'),
        ),
        migrations.AddField(
            model_name='serviceoption',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='orders.service', verbose_name='Название сервиса'),
        ),
        migrations.AddField(
            model_name='order',
            name='service_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.serviceoption', verbose_name='Опции'),
        ),
    ]

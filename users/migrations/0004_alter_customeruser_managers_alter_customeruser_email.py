# Generated by Django 5.1.1 on 2024-09-20 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customeruser_balance_customeruser_balance_currency'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customeruser',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='customeruser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-24 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_remove_service_description_remove_service_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceoption',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Категория'),
        ),
    ]

from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse


class Service(models.Model):
    name = models.CharField('Название услуги', max_length=50, db_index=True)
    slug = models.SlugField(
        'Слаг',
        max_length=255,
        unique=True, db_index=True,
        validators=[
            MinLengthValidator(5, "Минимум 5 символов"),
            MaxLengthValidator(100, "Максимум 50 символов"),
        ])

    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=3, default=0)

    category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, related_name='service', verbose_name="Категории"
    )

    tags = models.ManyToManyField('Tag', related_name='services')

    objects = models.Manager()

    class Meta:
        ordering = ('name',)
        indexes = [models.Index(fields=['name'])]  # ускоряет сортировку в таблице
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Название категории', max_length=100, db_index=True)
    slug = models.SlugField('Слаг', max_length=150, unique=True, db_index=True)

    objects = models.Manager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('service:category', kwargs={'category_slug': self.slug})

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ServiceDetail(models.Model):
    service = models.ForeignKey(Service, related_name='details', on_delete=models.CASCADE)
    detail = models.CharField(max_length=255)

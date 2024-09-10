from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomerUser(AbstractUser):
    email = models.EmailField(verbose_name='Email',
                              max_length=255,
                              unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

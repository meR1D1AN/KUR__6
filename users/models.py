from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="@Email")
    is_active = models.BooleanField(default=False, verbose_name="Активирован")

    token = models.CharField(
        max_length=100, verbose_name="Токен", null=True, blank=True
    )

    avatar = models.ImageField(
        upload_to="users/", verbose_name="Аватар", null=True, blank=True
    )
    phone = models.CharField(
        max_length=35, verbose_name="Телефон", null=True, blank=True
    )
    region = models.CharField(
        max_length=50, verbose_name="Регион", null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

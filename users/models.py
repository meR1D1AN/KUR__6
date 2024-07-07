from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="@Email")
    is_active = models.BooleanField(default=False, verbose_name="Активирован")
    token = models.CharField(unique=True, max_length=100, verbose_name="Токен", **NULLABLE)
    avatar = models.ImageField(upload_to="users/", verbose_name="Аватар", **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name="Телефон", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ('deactivate_user', 'Может деактивировать пользователя'),
            ('view_all_users', 'Может просматривать всех пользователей'),
        ]

    def __str__(self):
        return self.email

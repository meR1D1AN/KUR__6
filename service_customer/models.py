from datetime import datetime
from django.db import models

from users.models import User

NULLABLE = {"null": True, "blank": True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Введите электронную почту")
    full_name = models.CharField(max_length=255, verbose_name="Полное Ф.И.О.")
    comment = models.CharField(max_length=255, **NULLABLE, verbose_name="Комментарий")
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Владелец", **NULLABLE
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.full_name}"


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема")
    body = models.TextField(verbose_name="Текст")
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Владелец", **NULLABLE
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"{self.subject}"


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Начата"),
        ("finished", "Завершена"),
    ]
    # день = 1440 минут, неделя = 10080 минут, месяц = 43200 минут
    PERIODICITY_CHOICES = [
        (1440, "Каждый день"),
        (10080, "Каждую неделю"),
        (43200, "Каждый месяц"),
    ]
    active = models.BooleanField(verbose_name="Активна ли рассылка", blank=False)
    start_date = models.DateTimeField(
        default=datetime.now, verbose_name="Дата и время начала рассылки"
    )
    last_sent_date = models.DateTimeField(
        verbose_name="Дата и время последней рассылки", **NULLABLE
    )
    periodicity = models.IntegerField(
        choices=PERIODICITY_CHOICES,
        verbose_name="Периодичность рассылки",
        default="1440",
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        verbose_name="Статус рассылки",
        default="created",
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    clients = models.ManyToManyField(
        Client, related_name="mailings", verbose_name="Клиенты"
    )
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Владелец", **NULLABLE
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("deactivate_mailing", "Может деактивировать рассылку"),
            ("view_all_mailings", "Может просматривать все рассылки"),
        ]

    def __str__(self):
        return f"Рассылка {self.id} - {self.get_status_display()}"


class MailingAttempt(models.Model):
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, default=1, verbose_name="Рассылка"
    )
    attempt_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время начала рассылки"
    )
    status = models.CharField(max_length=50, verbose_name="Статус рассылки")
    server_response = models.TextField(**NULLABLE, verbose_name="Ответ сервера")
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=False
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        permissions = [
            ("view_mailing", "Может просматривать попытки рассылки"),
        ]

    def __str__(self):
        return f"Попытка {self.id} для рассылки {self.mailing.id}"

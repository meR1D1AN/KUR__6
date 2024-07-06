from datetime import datetime, timedelta
from django.db import models

NULLABLE = {"null": True, "blank": True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Введите электронную почту")
    full_name = models.CharField(max_length=255, verbose_name="Полное Ф.И.О.")
    comment = models.CharField(max_length=255, **NULLABLE, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.full_name}"


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема")
    body = models.TextField(verbose_name="Текст")

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
    PERIODICITY_CHOICES = [
        ("daily", "Каждый день"),
        ("weekly", "Каждую неделю"),
        ("monthly", "Каждый месяц"),
    ]
    ACTIVE_CHOICES = [
        (True, 'Да'),
        (False, 'Нет'),
    ]
    active = models.BooleanField(choices=ACTIVE_CHOICES, default=True, verbose_name="Активна ли подписка")
    start_date = models.DateTimeField(default=datetime.now, verbose_name="Дата и время начала рассылки")
    last_sent_date = models.DateTimeField(verbose_name="Дата и время последней рассылки", **NULLABLE)
    periodicity = models.CharField(
        max_length=50,
        choices=PERIODICITY_CHOICES,
        verbose_name="Периодичность рассылки",
        default="daily",
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        verbose_name="Статус рассылки",
        default="created",
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    clients = models.ManyToManyField(Client, related_name="mailings", verbose_name="Клиенты")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"Рассылка {self.id} - {self.status}"

    def periodicity_timedelta(self):
        if self.periodicity == "daily":
            return timedelta(seconds=10)
            # return timedelta(days=1)
        elif self.periodicity == "weekly":
            return timedelta(weeks=1)
        elif self.periodicity == "monthly":
            return timedelta(days=30)


class MailingAttempt(models.Model):
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, default=1, verbose_name="Рассылка"
    )
    attempt_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время начала рассылки"
    )
    status = models.CharField(max_length=50, verbose_name="Статус рассылки")
    server_response = models.TextField(**NULLABLE, verbose_name="Ответ сервера")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"

    def __str__(self):
        return f"Попытка {self.id} для рассылки {self.mailing.id}"

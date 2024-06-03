from datetime import datetime

from django.db import models


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Введите электронную почту')
    full_name = models.CharField(max_length=255, verbose_name='Полное Ф.И.О.')
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.full_name}'


class Message(models.Model):
    subject = models.CharField(max_length=255, unique=True, verbose_name='Тема')
    body = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.subject}'


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Начата'),
        ('finished', 'Завершена'),
    ]
    PERIODICITY_CHOICES = [
        ('daily', 'Каждый день'),
        ('weekly', 'Каждую неделю'),
        ('monthly', 'Каждый месяц'),
    ]

    start_date = models.DateTimeField(default=datetime.now)
    periodicity = models.CharField(max_length=50, choices=PERIODICITY_CHOICES, default='daily')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, related_name='mailings')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f"Mailing {self.id} - {self.status}"


class MailingAttempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, default=1)
    attempt_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    server_response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Attempt {self.id} for Mailing {self.mailing.id}"

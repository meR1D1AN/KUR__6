from django.db import models
from django.utils.text import slugify

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    full_name = models.CharField(max_length=254, verbose_name='Полное имя')
    comment = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'

    def __str__(self):
        return self.full_name


class MailingList(models.Model):
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='Время начала рассылки')
    FREQUENCY_CHOICES = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, verbose_name='Периодичность рассылки')
    STATUS_CHOICES = [
        ('created', 'Создан'),
        ('started', 'Запущен'),
        ('completed', 'Завершено'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус рассылки')
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='Сообщение')
    clients = models.ManyToManyField('Client')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return self.frequency


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Текст письма')

    class Meta:
        verbose_name = 'Сообщение рассылки'
        verbose_name_plural = 'Сообщения рассылки'

    def __str__(self):
        return self.subject


class MailingAttempt(models.Model):
    mailing = models.ForeignKey('MailingList', on_delete=models.CASCADE, verbose_name='Рассылка')
    attempt_time = models.DateTimeField()
    STATUS_CHOICES = [
        ('successful', 'Успешно'),
        ('failed', 'Не успешно'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус попытки рассылки')
    server_response = models.TextField(**NULLABLE, verbose_name='Ответ сервера')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

    def __str__(self):
        return self.status

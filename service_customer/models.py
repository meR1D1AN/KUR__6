from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')
    email = models.EmailField(verbose_name='Электронная почта')
    comment = models.TextField(verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'

    def __str__(self):
        return f'{self.name} {self.surname} {self.patronymic}'


class MailingList(models.Model):
    send_date_mailing = models.DateTimeField(verbose_name='Дата рассылки')
    periodicity = models.IntegerField(verbose_name='Периодичность рассылки')
    mailing_status = models.BooleanField(verbose_name='Статус рассылки', default=False)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'{self.send_date_mailing}'


class MessageMailing(models.Model):
    email_subject = models.CharField(max_length=100, verbose_name='Тема письма')
    email_text = models.TextField(verbose_name='Текст письма')
    mailing = models.ForeignKey(MailingList, on_delete=models.CASCADE, verbose_name='Рассылка')

    class Meta:
        verbose_name = 'Сообщение рассылки'
        verbose_name_plural = 'Сообщения рассылки'

    def __str__(self):
        return f'{self.email_subject}'


class MailingAttempted(models.Model):
    date_and_time_of_last_attempt = models.DateTimeField(verbose_name='Дата и время последнего попытки рассылки')
    status_attempt = models.BooleanField(verbose_name='Статус попытки рассылки', default=False)
    mail_service_response = models.CharField(max_length=100, verbose_name='Ответ сервера', **NULLABLE)

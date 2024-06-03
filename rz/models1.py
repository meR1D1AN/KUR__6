from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'

    def __str__(self):
        return f'{self.full_name}'


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
    date_and_time_of_last_attempt = models.DateTimeField(auto_now_add=True,
                                                         verbose_name='Дата и время последнего попытки рассылки')
    status_attempt = models.CharField(max_length=50, choices=[('successful', 'Успешно'), ('failed', 'Не успешно')],
                                      verbose_name='Статус попытки рассылки')
    mail_service_response = models.TextField(verbose_name='Ответ сервера', **NULLABLE)
    mailing = models.ForeignKey(MailingList, on_delete=models.CASCADE)


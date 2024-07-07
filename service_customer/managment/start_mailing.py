import smtplib
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

from service_customer.models import Mailing, MailingAttempt


class Command(BaseCommand):

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status='Запущена')

        for mailing in mailings:
            clients = mailing.clients.all()
            try:
                send_mail(
                    subject=mailing.message.title,
                    message=mailing.message.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in clients],
                    fail_silently=False,
                )
                status = "Успешная рассылка"
                server_response = "Электронное письмо успешно отправлено."

            except smtplib.SMTPException as e:
                status = "Отказ"
                server_response = str(e)

            MailingAttempt.objects.create(
                mailing=mailing, status=status, server_response=server_response, owner=mailing.owner
            )

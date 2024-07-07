import smtplib
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.conf import settings
from service_customer.models import Mailing, MailingAttempt
import pytz


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    # Завершение рассылок, которые стали неактивными
    inactive_mailings = Mailing.objects.filter(active=False, status__in=["created", "started"])
    for mailing in inactive_mailings:
        mailing.status = "finished"
        mailing.save()

    created_mailings = Mailing.objects.filter(active=True, status="created")
    for mailing in created_mailings:
        clients = mailing.clients.all()
        for client in clients:
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
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

        # Обновление статуса рассылки и даты последней рассылки
        mailing.status = "started"
        mailing.last_sent_date = current_datetime
        mailing.save()

    # Рассылка, если активна и начата
    started_mailings = Mailing.objects.filter(active=True, status="started")
    for mailing in started_mailings:
        if mailing.last_sent_date is None:
            time_diff = (current_datetime - mailing.start_date).total_seconds()
        else:
            time_diff = (current_datetime - mailing.last_sent_date).total_seconds()
        if time_diff >= mailing.periodicity * 60:
            clients = mailing.clients.all()
            for client in clients:
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
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

            # Обновление даты последней рассылки
            mailing.last_sent_date = current_datetime
            mailing.save()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, "interval", minutes=1)
    scheduler.start()

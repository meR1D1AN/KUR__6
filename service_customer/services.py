from django.core.mail import send_mail
from django.conf import settings
from service_customer.models import Mailing, MailingAttempt
from datetime import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = Mailing.objects.filter(start_date__lte=current_datetime).filter(status="created").filter(active=True)

    for mailing in mailings:
        if not mailing.active:
            mailing.status = "finished"
            continue
        clients = mailing.clients.all()
        for client in clients:
            # Проверьте, прошло ли указанное время с момента последней рассылки
            if mailing.last_sent_date is None or (
                    current_datetime - mailing.last_sent_date) >= mailing.periodicity_timedelta():
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                        fail_silently=False,
                    )
                    status = "started"
                    server_response = "Электронное письмо успешно отправлено."
                except Exception as e:
                    status = "Отказ"
                    server_response = str(e)

                MailingAttempt.objects.create(
                    mailing=mailing, status=status, server_response=server_response
                )

                # Обновление поля даты последней рассылки
                mailing.last_sent_date = current_datetime
                mailing.save()

                # Обновления статуса рассылки
                mailing.status = "started"
                mailing.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, "interval", minutes=1)
    scheduler.start()

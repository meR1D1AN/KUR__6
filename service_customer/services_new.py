from django.core.mail import send_mail
from django.conf import settings
from service_customer.models import Mailing, MailingAttempt
from datetime import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
import logging

logger = logging.getLogger(__name__)


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = Mailing.objects.filter(start_date__lte=current_datetime).filter(status="created").filter(active=True)

    for mailing in mailings:
        if mailing.active:
            clients = mailing.clients.all()
            for client in clients:
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
        else:
            mailing.status = "finished"
            mailing.save()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(send_mailing, "interval", seconds=60, id="send_mailing", replace_existing=True)
    register_events(scheduler)
    scheduler.start()
    logger.info("Scheduler started.")

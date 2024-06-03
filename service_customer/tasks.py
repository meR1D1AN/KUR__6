from django.core.mail import send_mail
from django.conf import settings
from service_customer.models import Mailing, MailingAttempt
from datetime import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = Mailing.objects.filter(start_date__lte=current_datetime).filter(status='created')

    for mailing in mailings:
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
                status = 'Success'
                server_response = 'Email sent successfully.'
            except Exception as e:
                status = 'Failure'
                server_response = str(e)

            MailingAttempt.objects.create(
                mailing=mailing,
                status=status,
                server_response=server_response
            )

        # Update the status of the mailing
        mailing.status = 'finished'
        mailing.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', minutes=1)
    scheduler.start()

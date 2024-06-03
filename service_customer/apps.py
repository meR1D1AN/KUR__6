from django.apps import AppConfig
import time


class ServiceCustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service_customer'

    def ready(self):
        from .tasks import start
        time.sleep(2)
        start()

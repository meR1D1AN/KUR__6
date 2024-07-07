from django.apps import AppConfig
import time


class ServiceCustomerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "service_customer"

    def ready(self):
        from service_customer.services import start_scheduler
        time.sleep(2)
        start_scheduler()

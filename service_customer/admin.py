from django.contrib import admin
from service_customer.models import Client, Message, Mailing, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "comment")
    search_fields = ("full_name", "email")
    list_filter = ("full_name", "email")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")
    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_date", "last_sent_date", "active", "periodicity", "status", "message", "owner")
    search_fields = ("status", "message__subject")
    list_filter = ("status", "periodicity", "start_date", "active")
    filter_horizontal = ("clients",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "mailing", "attempt_date", "status", "server_response")
    search_fields = ("status", "mailing__id")
    list_filter = ("status", "attempt_date")

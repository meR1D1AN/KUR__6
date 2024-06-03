from django.contrib import admin
from rz.models import *


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment',)
    list_filter = ('full_name')
    search_fields = ('email', 'full_name',)


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'frequency', 'status', 'message')
    list_filter = ('frequency', 'status')
    search_fields = ('message__subject',)
    filter_horizontal = ('clients',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')
    search_fields = ('subject', 'body')


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('servicemailing', 'attempt_time', 'status', 'server_response')
    list_filter = ('status',)
    search_fields = ('mailing__message__subject',)



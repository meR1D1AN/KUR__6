from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from service_customer.forms import MailingForm
from service_customer.models import *


class HomeView(TemplateView):
    template_name = "service_customer/home.html"


# Client Views
class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ["email", "full_name", "comment"]

    def get_success_url(self):
        return reverse_lazy("service_customer:client_list")


class ClientUpdateView(UpdateView):
    model = Client
    fields = ["email", "full_name", "comment"]

    def get_success_url(self):
        return reverse_lazy("service_customer:client_list")


class ClientDeleteView(DeleteView):
    model = Client

    def get_success_url(self):
        return reverse_lazy("service_customer:client_list")


# Message Views
class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = ("subject", "body")

    def get_success_url(self):
        return reverse_lazy("service_customer:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    fields = ("subject", "body")

    def get_success_url(self):
        return reverse_lazy("service_customer:message_list")


class MessageDeleteView(DeleteView):
    model = Message

    def get_success_url(self):
        return reverse_lazy("service_customer:message_list")


# Mailing Views
class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        return Mailing.objects.all().order_by('-id')


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy("service_customer:mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy("service_customer:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing

    def get_success_url(self):
        return reverse_lazy("service_customer:mailing_list")


class MailingAttemptListView(ListView):
    model = MailingAttempt


class MailingAttemptDetailView(DetailView):
    model = MailingAttempt


class MailingAttemptDeleteView(DeleteView):
    model = MailingAttempt

    def get_success_url(self):
        return reverse_lazy("service_customer:mailing_attempt_list")

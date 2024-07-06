from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

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


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    fields = ["start_date", "periodicity", "status", "message", "clients", "active"]

    def get_success_url(self):
        return reverse_lazy("service_customer:mailing_list")

    def post(self, request):
        active = request.POST.get("active")
        if active == "on":
            active = True
        else:
            active = False
        start_date = request.POST.get("start_date")
        last_sent_date = request.POST.get("last_sent_date")
        periodicity = request.POST.get("periodicity")
        status = request.POST.get("status")
        message_id = request.POST.get("message")
        client_ids = request.POST.getlist("clients")

        start_date = timezone.make_aware(
            datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        )

        message = Message.objects.get(id=message_id)
        mailing = Mailing.objects.create(
            active=active,
            start_date=start_date,
            last_sent_date=last_sent_date,
            periodicity=periodicity,
            status=status,
            message=message,
        )

        for client_id in client_ids:
            client = Client.objects.get(id=client_id)
            mailing.clients.add(client)

        mailing.save()
        return redirect("service_customer:mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ["start_date", "periodicity", "status", "message", "clients", "active"]

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

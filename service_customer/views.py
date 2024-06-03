from django.shortcuts import redirect, render
from django.urls import reverse_lazy
# from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from service_customer.models import *


class HomeView(TemplateView):
    template_name = 'service_customer/base.html'


# Client Views
class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']

    def get_success_url(self):
        return reverse_lazy('service_customer:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']

    def get_success_url(self):
        return reverse_lazy('service_customer:client_list')


class ClientDeleteView(DeleteView):
    model = Client

    def get_success_url(self):
        return reverse_lazy('service_customer:client_list')


# Message Views
class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = ('subject', 'body')

    def get_success_url(self):
        return reverse_lazy('service_customer:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('subject', 'body')

    def get_success_url(self):
        return reverse_lazy('service_customer:message_list')


class MessageDeleteView(DeleteView):
    model = Message

    def get_success_url(self):
        return reverse_lazy('service_customer:message_list')


# Mailing Views
class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['start_date', 'periodicity', 'status', 'message', 'clients']

    # def get_success_url(self):
    #     return reverse_lazy('service_customer:mailing_list')

    def get(self, request):
        messages = Message.objects.all()
        clients = Client.objects.all()
        return render(request, 'service_customer/mailing_create.html', {'messages': messages, 'clients': clients})

    def post(self, request):
        start_date = request.POST.get('start_date')
        periodicity = request.POST.get('periodicity')
        status = request.POST.get('status')
        message_id = request.POST.get('message')
        client_ids = request.POST.getlist('clients')

        message = Message.objects.get(id=message_id)
        mailing = Mailing.objects.create(start_date=start_date, periodicity=periodicity, status=status, message=message)

        for client_id in client_ids:
            client = Client.objects.get(id=client_id)
            mailing.clients.add(client)

        mailing.save()
        return redirect('service_customer:mailing_list')

    # def form_valid(self, form):
    #     mailing = form.save(commit=False)
    #     mailing.user = self.request.user
    #
    #     # Проверяем, что выбранный пользователь не имеет рассылки с такой же периодичностью
    #     if Mailing.objects.filter(Q(user=mailing.user) & Q(periodicity=mailing.periodicity)).exists():
    #         form.add_error(None, "Выбранный пользователь уже имеет рассылку с такой же периодичностью.")
    #         return self.form_invalid(form)
    #
    #     mailing.save()
    #     return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['start_date', 'periodicity', 'status', 'message', 'clients']

    def get_success_url(self):
        return reverse_lazy('service_customer:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing

    def get_success_url(self):
        return reverse_lazy('service_customer:mailing_list')

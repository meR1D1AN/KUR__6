from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rz.models import *


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client
    slug_url_kwarg = 'slug'


class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('servicemailing:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    slug_url_kwarg = 'slug'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('servicemailing:client_list')

    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(DeleteView):
    model = Client
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('servicemailing:client_list')


class MailingListListView(ListView):
    model = MailingList


class MailingListDetailView(DetailView):
    model = MailingList
    slug_url_kwarg = 'slug'


class MailingListCreateView(CreateView):
    model = MailingList
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('servicemailing:mailinglist_list')


class MailingListUpdateView(UpdateView):
    model = MailingList
    slug_url_kwarg = 'slug'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('servicemailing:mailinglist_list')

    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'pk': self.object.pk})


class MailingListDeleteView(DeleteView):
    model = MailingList
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('servicemailing:mailinglist_list')


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message
    slug_url_kwarg = 'slug'


class MessageCreateView(CreateView):
    model = Message
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('servicemailing:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    slug_url_kwarg = 'slug'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('servicemailing:message_list')

    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('servicemailing:message_list')


class MailingAttemptListView(ListView):
    model = MailingAttempt


class MailingAttemptDetailView(DetailView):
    model = MailingAttempt
    slug_url_kwarg = 'slug'


class MailingAttemptCreateView(CreateView):
    model = MailingAttempt
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('servicemailing:mailingattempt_list')


class MailingAttemptUpdateView(UpdateView):
    model = MailingAttempt
    slug_url_kwarg = 'slug'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('service_customer:mailingattempt_list')

    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'pk': self.object.pk})


class MailingAttemptDeleteView(DeleteView):
    model = MailingAttempt
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('servicemailing:mailingattempt_list')

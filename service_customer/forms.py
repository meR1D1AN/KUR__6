from django import forms
from service_customer.models import Mailing


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['active', 'start_date', 'periodicity', 'status', 'clients', 'message']

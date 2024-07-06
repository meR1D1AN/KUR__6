from django import forms
from service_customer.models import Client, Mailing, MailingAttempt


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['active', 'start_date', 'last_sent_date', 'periodicity', 'status', 'message', 'clients']

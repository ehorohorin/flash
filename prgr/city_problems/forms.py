from django.forms import ModelForm
from .models import Problem

class ContactForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['status', 'short_name']

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        print("Success post")
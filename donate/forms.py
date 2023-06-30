from django import forms
from django.core.exceptions import ValidationError

from donate.models import Donation


class DonationForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = Donation
        fields = ['quantity']


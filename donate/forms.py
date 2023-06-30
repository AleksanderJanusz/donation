from django import forms
from django.core.exceptions import ValidationError
from donate.models import Donation


class DonationForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)
    pick_up_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    pick_up_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    pick_up_comment = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}))

    class Meta:
        model = Donation
        fields = ['quantity', 'address', 'phone_number', 'city', 'zip_code', 'pick_up_date', 'pick_up_time',
                  'pick_up_comment']
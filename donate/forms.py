from django import forms
from django.core.exceptions import ValidationError
from donate.models import Donation
from phonenumber_field.formfields import PhoneNumberField


class DonationForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)
    pick_up_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    pick_up_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    phone_number = PhoneNumberField(region='PL')

    def clean(self):
        cleaned_data = super().clean()
        zip_code = cleaned_data['zip_code']
        if zip_code[2] == '-':
            zip_code = zip_code.replace('-', '')
        if len(zip_code) != 5:
            raise ValidationError(f'Kod pocztowy nie poprawny1{zip_code}')
        try:
            zip_code = int(zip_code)
        except ValueError:
            raise ValidationError('Kod pocztowy nie poprawny2')
        return cleaned_data

    class Meta:
        model = Donation
        widgets = {'pick_up_comment': forms.Textarea(attrs={'rows': 5})}
        fields = ['quantity', 'address', 'phone_number', 'city', 'zip_code', 'pick_up_date', 'pick_up_time',
                  'pick_up_comment']

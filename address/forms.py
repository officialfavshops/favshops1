from django import forms
from .models import Address

class address_form(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('at','post','panchayat','dist','pin','state','alternate_number')
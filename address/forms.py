from django import forms
from .models import Address

class address_form(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('full_name','at','landmark','panchayat','dist','pin','state','alternate_number')
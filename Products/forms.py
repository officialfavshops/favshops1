from django import forms
from .models import Product

class Product_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','brand','quantity','image','retail_price','margin_price','actual_price','discount_price','discount_percentage','description','quality','category','special_offer','best_offer')
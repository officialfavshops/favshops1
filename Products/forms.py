from django import forms
from .models import Product

class Product_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('image','product_name','brand','quantity','retail_price','margin_price','mrp','description','quality','category','special_offer','best_offer','out_of_stock')
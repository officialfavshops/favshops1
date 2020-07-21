from django.db import models
from Products.models import Product
# Create your models here.
class Cart(models.Model):
    mobile_number = models.CharField(max_length=20,null=True,blank=True)
    product = models.ForeignKey(Product,null=True,blank=True,on_delete=models.SET_NULL)
    customer_quantity = models.CharField(max_length=30,null=False,blank=False,default=1)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


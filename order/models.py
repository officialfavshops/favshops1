from django.db import models
from cart.models import Cart
from address.models import Address
from User.models import User
from django.utils import timezone
# Create your models here.
class Order(models.Model):

    order_id = models.CharField(max_length=30,null=True,blank=True)
    image = models.ImageField(upload_to='order_history_img',null=True,blank=True)
    mobile_number = models.CharField(max_length=15,null=True,blank=True)
    name = models.CharField(max_length=30,null=True,blank=True)
    brand = models.CharField(max_length=40,blank=True,null=True)
    quantity = models.CharField(max_length=20,null=True,blank=True)
    customer_quantity = models.CharField(max_length=30,null=False,blank=False,default=1)
    price = models.CharField(max_length=20,null=True,blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    payment_mode = models.CharField(max_length=30,null=True,blank=True)
    packed = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    order_canceled = models.BooleanField(default=False)
    status = models.CharField(max_length=30,null=True,blank=True)
    delivered_date = models.DateTimeField(null=True,blank=True)
    margin_price = models.CharField(max_length=100,null=True,blank=True)


class Admin_order_summary(models.Model):
    order_id = models.CharField(max_length=50,null=True,blank=True)
    order_items = models.CharField(max_length=1000,null=True,blank=True)
    cancel_items = models.CharField(max_length=1000,null=True,blank=True)
    total_price = models.CharField(max_length=100,null=True,blank=True)
    payment_mode = models.CharField(max_length=50,null=True,blank=True)
    order_address = models.CharField(max_length=200,null=True,blank=True)
    order_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    delivered_by = models.CharField(max_length=70,null=True,blank=True)
    order_time = models.DateTimeField(null=True,blank=True)
    delivered_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=timezone.now)
    total_margin = models.CharField(max_length=100,null=True,blank=True)
    delivery_charges = models.CharField(max_length=100,null=True,blank=True)



from django.contrib import admin
from .models import Order,Admin_order_summary
# Register your models here.
admin.site.register(Order)
admin.site.register(Admin_order_summary)
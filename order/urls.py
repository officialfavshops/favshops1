from django.urls import path
from . import views

urlpatterns = [
    path('cancel_order/<int:pk>/',views.cancel_order,name='order/cancel_order'),
    path('delete_delivery_item/<int:pk>/',views.delete_delivery_item,name='delete_delivery_item'),
    path('delete_packed_item/<int:pk>/',views.delete_packed_item,name='delete_packed_item'),
    path('order_delivered',views.order_delivered,name='order_delivered'),
    path('admin_order_summary',views.admin_order_summary,name='admin_order_summary'),
]

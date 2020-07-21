from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/<int:pk>/',views.add_to_cart,name='add_to_cart'),
    path('delete_cart_item/<int:pk>/',views.delete_cart_item,name='delete_cart_item'),
    path('change_quantity',views.change_quantity,name='change_quantity'),
    path('cart_checkout',views.cart_checkout,name='cart_checkout'),
    path('handlerequest/',views.handlerequest,name='HandleRequest'),
    path('payment_mode',views.payment_mode,name='payment_mode'),
    path('add_to_cart_ajax',views.add_to_cart_ajax,name='add_to_cart_ajax'),
]

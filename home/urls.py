from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('user_register',views.user_register,name='user_register'),
    path('user_login',views.user_login,name='user_login'),
    path('wish_list',views.wish_list,name='wish_list'),
    path('forget_password',views.forget_password,name='forget_password'),
    path('admin_page',views.admin_page,name='admin_page'),
    path('cart_page',views.cart_page,name='cart_page'),
    path('about',views.about,name='about'),
    path('order_history',views.order_history,name='order_history'),
    path('contact',views.contact,name='contact'),
    path('profile_page',views.profile_page,name='profile_page'),
    path('product_details/<int:pk>/',views.product_details,name='product_details'),
    path('delivery_boy_page',views.delivery_boy,name='delivery_boy_page'),
    path('not_delivered',views.not_delivered,name='not_delivered'),
    path('order_packed/<int:pk>/',views.order_packed,name='order_packed'),
    
]
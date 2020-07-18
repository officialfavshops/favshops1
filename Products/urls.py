from django.urls import path
from . import views


urlpatterns = [
    path('add_products',views.add_products,name='add_products'),
    path('all_products',views.all_products,name='all_products'),
    path('edit_product/<int:pk>/',views.edit_product,name='edit_product'),
    path('delete_product/<int:pk>/',views.delete_product,name='delete_product'),
]

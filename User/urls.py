from django.urls import path
from . import views

urlpatterns = [
    path('user/register',views.register,name='user/register'),
    path('user/login',views.login,name='user/login'),
    path('validate_mobileno',views.validate_mobileno,name='validate_mobileno'),
    path('validate_email',views.validate_email,name='validate_email'),
    path('user_logout',views.logout,name='user_logout'),
    path('verify_forget_password',views.verify_forget_password,name='verify_forget_password'),
    path('forget_password_ajax',views.forget_password_ajax,name='forget_password_ajax'),
]

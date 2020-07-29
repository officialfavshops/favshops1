from django.shortcuts import render,redirect
from .models import User
from django.contrib.auth.models import auth
from django.http import JsonResponse
from home.views import user_login
#from django.contrib.auth import authenticate,login
# Create your views here.
from random import sample
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        mobile_number = request.POST['mobile_number']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.create_user(mobile_number=mobile_number,first_name=first_name,last_name=last_name,email=email,password=password,confirm_password=confirm_password)
        print(user.password,user.confirm_password)
        user.save()
        return redirect('user_login')
    else:
        return render(request,'register.html')

def login(request):
    messages = ''
    if request.method == 'POST':
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']

        user = auth.authenticate(mobile_number = mobile_number,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages += 'Incorrect Mobile number or Password'
            return render(request,'login.html',{'messages':messages})
    else:
        return render(request,'login.html')

def validate_mobileno(request):
    mobile_number = request.GET.get('mobile_number',None)
    data = {
        'is_taken' : User.objects.filter(mobile_number__iexact=mobile_number).exists()
    }
    print(mobile_number)
    print('Exist :',data['is_taken'])
    return JsonResponse(data)

def validate_email(request):
    email = request.GET.get('email',None)
    data = {
        'is_taken' : User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)

def logout(request):
    auth.logout(request)
    return redirect('/')

def send_otp(request):
    mobile_number = request.POST['forget_mobile_number']
    message = ' '
    user = User.objects.get(mobile_number__iexact = mobile_number)
    email = user.email
    list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','a','b','c','x','y','z','0','1','2','3','4','5','6','7','8','9']
    otp = sample(list,4)
    otp_str = ''.join(otp)
    subject = 'FAVShops : Reset Password'
    msg = 'Your OTP to reset your Account Password is : '+ str(otp_str)
    sender = 'officialfavshops@gmail.com'
    receiver = email
    send_mail(subject,msg,sender,[receiver],fail_silently=False)

    return render(request,'verify_otp.html',{'email':email,'otp':otp_str,'mobile_number':user.mobile_number})

def forget_password_ajax(request):
    
    number = request.GET.get('number',None)
    data = {
            'exist_num' : User.objects.filter(mobile_number__iexact = number).exists(),
            'length': len(number)
        }
    return JsonResponse(data)

def verify_otp(request):
    message = ''
    otp = request.POST['otp']
    user_otp = request.POST['user_otp']
    mobile_number = request.POST['mobile_number']
    if otp == user_otp:
        return render(request,'change_password.html',{'mobile_number':mobile_number})
    else:
        pass

def save_new_password(request):
    mobile_number = request.POST['mobile_number']
    password = request.POST['password']

    user = User.objects.get('mobile_number' == mobile_number)
    user.set_password(password)
    user.confirm_password = password
    user.save()
    return redirect('user/login')
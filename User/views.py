from django.shortcuts import render,redirect
from .models import User
from django.contrib.auth.models import auth
from django.http import JsonResponse
from home.views import user_login
#from django.contrib.auth import authenticate,login
# Create your views here.

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

def verify_forget_password(request):
    mobile_number = request.POST['forget_mobile_number']
    message = ' '
    user = User.objects.get(mobile_number__iexact = mobile_number)
    email = user.email
    return redirect(request,'verify_otp.html',{'email':email})

def forget_password_ajax(request):
    
    number = request.GET.get('number',None)
    data = {
            'exist_num' : User.objects.filter(mobile_number__iexact = number).exists(),
            'length': len(number)
        }
    return JsonResponse(data)

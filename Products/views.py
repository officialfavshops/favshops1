from django.shortcuts import render,redirect
from .forms import Product_form
from .models import Product
from django.contrib import messages
import math


# Create your views here.

def add_products(request):
    
    if request.method == 'POST':
        form = Product_form(request.POST or None,request.FILES or None)
        if form.is_valid():
            product = form.save(commit=False)
            #dis_price = int(form.cleaned_data['discount_price'])
            act_price = float(form.cleaned_data['mrp'])
            mrg_price =float(form.cleaned_data['margin_price'])
            rtl_price = float(form.cleaned_data['retail_price'])
            discount_price = float(mrg_price) + float(rtl_price)
            product.discount_price = str(discount_price)
            per = math.round(((discount_price / act_price) * 100))
            per = 100 - per
            product.discount_percentage = per
            product.save()
            name = form.cleaned_data['product_name']
            msg = '%s Added Successfully ..'%name
            messages.success(request, msg)
            return redirect('all_products')
    else:
        form = Product_form()
    return render(request,'add_products.html',{'form':form,})

def all_products(request):
    products = Product.objects.all().order_by('-upload_time')
    total_product = len(products)

    return render(request,'admin_page.html',{'products':products,'total_products':total_product})

def edit_product(request,pk):
    products = Product.objects.all()
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
       product_edit_form = Product_form(request.POST or None,request.FILES or None,instance=product)
       if product_edit_form.is_valid():
           product = product_edit_form.save(commit=False)
           # dis_price = int(form.cleaned_data['discount_price'])
           act_price = float(product_edit_form.cleaned_data['mrp'])
           mrg_price = float(product_edit_form.cleaned_data['margin_price'])
           rtl_price = float(product_edit_form.cleaned_data['retail_price'])
           discount_price = float(mrg_price) + float(rtl_price)
           product.discount_price = str(discount_price)
           per = ((discount_price / act_price) * 100)
           per = 100 - per
           product.discount_percentage = per
           product.save()
           name = product_edit_form.cleaned_data['product_name']
           msg = '%s Edited Successfully ..' % name
           messages.success(request, msg)
           return redirect('all_products')
    else:
        product_edit_form = Product_form(instance=product)
   
    return render(request,'edit_product.html',{'product_edit_form':product_edit_form})

def delete_product(request,pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('all_products')


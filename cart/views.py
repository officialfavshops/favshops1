from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from Products.models import Product
from .models import Cart
from address.forms import address_form
from address.models import Address
from order.models import Order

from User.models import User
from django.views.decorators.csrf import csrf_exempt
from .paytm import Checksum
import math
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


#MERCHENTID = 'rJXvah34753603915703'
MERCHANTKEY = 'hTF&Qc@AU9Vf_NdM'

orderid = 'FAV0000'

# Create your views here.
def add_to_cart(request,pk):
    product = Product.objects.get(pk=pk)
    mobile_number = request.user.mobile_number
    cart = Cart.objects.create(mobile_number=mobile_number,product=product)
    cart.save()
    #request.user.save()
    #total_cart = len(request.user.cart)
    #print(total_cart)
    #print(request.user.cart)
    return redirect('index')


def add_to_cart_ajax(request):

    pk = request.GET.get('id',None)
    product = Product.objects.get(pk=pk)
    mobile_number = request.user.mobile_number
    total_cart = Cart.objects.filter(mobile_number=mobile_number)
    cart = Cart.objects.create(mobile_number=mobile_number,product=product)
    cart.save()
    new_total_cart = Cart.objects.filter(mobile_number=mobile_number)
    print('Cart Added')
    pname = product.product_name

    data={
            'added': ['True' if len(new_total_cart) > len(total_cart) else 'False'],
            'cart_len':len(new_total_cart),
            'pname':pname
        }
    return JsonResponse(data)


def delete_cart_item(request,pk):
    cart_product = Cart.objects.get(pk=pk)
    cart_product.delete()
    return redirect('cart_page')

def change_quantity(request):
    pk = request.GET.get('pk',None)
    val = request.GET.get('val',None)
    cart_item = Cart.objects.get(pk=pk)
    cart_item.customer_quantity = val
    cart_item.save()
    mnumber = request.user.mobile_number
    total = 0.0
    cart = Cart.objects.filter(mobile_number = mnumber).order_by('-add_time')
    for data in cart:
        total += float(data.product.discount_price) * float(data.customer_quantity)
    data = {
        'updated':True,
        'total':total
    }
    return JsonResponse(data)

def cart_checkout(request):
    mnumber = request.user.mobile_number
    fname = request.user.first_name
    lname = request.user.last_name
    total = 0
    delivery_charge = 0
    total_mrp_price = 0.0
    cart = Cart.objects.filter(mobile_number = mnumber).order_by('-add_time')
    address = Address.objects.filter(mobile_number = mnumber).first()
    total_product = len(cart)
    for data in cart:
        total += float(data.product.discount_price) * float(data.customer_quantity)
        total_mrp_price += float(data.product.mrp) * float(data.customer_quantity)

    you_save = total_mrp_price - total
    you_save_percentage = round((you_save / total_mrp_price) * 100)


    if total <= 100:
        delivery_charge = 10
    elif total > 100 and total <= 200:
        delivery_charge = 15
    elif total > 200 and total <= 350:
        delivery_charge = 20
    elif total > 350 and total <= 500:
        delivery_charge = 25
    else:
        delivery_charge = 0

    final_price = delivery_charge + total
    final_price = math.floor(final_price)

    if request.method == 'POST':
        total = 0.0
        total_mrp_price = 0.0
        number = request.user.mobile_number
        if address:
            form = address_form(request.POST or None,instance=address)
        else:
            form = address_form(request.POST or None)

        for data in cart:
            total += float(data.product.discount_price) * float(data.customer_quantity)
            total_mrp_price += float(data.product.mrp) * float(data.customer_quantity)

        you_save = total_mrp_price - total
        you_save_percentage = round((you_save / total_mrp_price) * 100)

        if total <= 100:
            delivery_charge = 10
        elif total > 100 and total <= 200:
            delivery_charge = 15
        elif total > 200 and total <= 350:
            delivery_charge = 20
        elif total > 350 and total <= 500:
            delivery_charge = 25
        else:
            delivery_charge = 0

        final_price = delivery_charge + total

        if form.is_valid():
            addr = form.save(commit=False)
            addr.mobile_number = mnumber
            addr.save()
            full_name = form.cleaned_data['full_name']
            at = form.cleaned_data['at']
            landmark = form.cleaned_data['landmark']
            panchayat = form.cleaned_data['panchayat']
            pin = form.cleaned_data['pin']
            dist = form.cleaned_data['dist']
            state = form.cleaned_data['state']

            al_number = form.cleaned_data['alternate_number']
            if al_number:
                pass
            else:
                al_number = ","

            total_address = full_name + " , " + at + " , " + landmark + " , " + panchayat + " , " + dist + " , " + pin + " , " + state + " , " + al_number
            return render(request,'payment_page.html',{'total':total,'delivery_charge':delivery_charge,'final_price':final_price,'address':total_address,'total_product':total_product,'you_save':you_save,'you_save_percentage':you_save_percentage,'total_mrp_price':total_mrp_price})
    else:
        form = address_form(instance=address)
    return render(request,'checkout_page.html',{'total':total,'delivery_charge':delivery_charge,'final_price':final_price,'total_product':total_product,'form':form,'you_save':you_save,'you_save_percentage':you_save_percentage,'total_mrp_price':total_mrp_price})




#def cart_checkout(request):
    #mnumber = request.user.mobile_number
    #total = 0
    #param_dict = {}

    #cart = Cart.objects.filter(mobile_number = mnumber).order_by('-add_time')
    #address = Address.objects.filter(mobile_number = mnumber).first()
    #total_product = len(cart)
    #for data in cart:
            #total += int(data.product.discount_price) * int(data.product.quantity.split(' ')[0])


    #if request.method == 'POST':
        #total = 0
        #number = request.user.mobile_number
        #if address:
            #form = address_form(request.POST or None,instance=address)
        #else:
            #form = address_form(request.POST or None)

        #for data in cart:
            #print(data.product.discount_price)
            #total += int(data.product.discount_price)
        #print(total)
        #if form.is_valid():
            #addr = form.save(commit=False)
            #addr.mobile_number = mnumber
            #addr.save()
            #at = form.cleaned_data['at']
            #post = form.cleaned_data['post']
            #panchayat = form.cleaned_data['panchayat']
            #pin = form.cleaned_data['pin']
            #dist = form.cleaned_data['dist']
            #state = form.cleaned_data['state']
            #address = at + " , " + post + " , " + panchayat + " , " + dist + " , " + pin + " , " + state
            #obj = Order()
            #order_id = obj.generate_id()
            #print(total)
            #data_dict = {
                #'MID': 'rJXvah34753603915703',
                #'ORDER_ID': str(order_id),
                #'TXN_AMOUNT': str(total),
                #'CUST_ID': request.user.email,
                #'INDUSTRY_TYPE_ID': 'Retail',
                #'WEBSITE': 'DEFAULT',
                #'CHANNEL_ID': 'WEB',
                #'CALLBACK_URL':'http://localhost:8000/cart/handlerequest/',
            #}
            #param_dict = data_dict
            #param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANTKEY)
            #return render(request, 'paytm.html', {'param_dict': param_dict})

    #else:
        #form = address_form(instance = address)

    #return render(request,'checkout_page.html',{'total':total,'form':form,'total_product':total_product})




def generate_id():
    order = Order.objects.order_by('-order_date')
    if order:
        order = order[0]
        orderid = order.order_id
        new_id = orderid[:3] + str(int(orderid[3:]) + 1 ).zfill(4)
        return new_id
    else:
        return 'FAV0001'


def create_order_paytm(request):
    mnumber = request.user.mobile_number
    total = 0.0
    delivery_charge = 0
    cart = Cart.objects.filter(mobile_number = mnumber).order_by('-add_time')
    address = Address.objects.filter(mobile_number = mnumber).first()
    al_number = ","
    if address.alternate_number:
        al_number = address.alternate_number
    full_name = address.full_name

    total_address = full_name + " , " + address.at + " , " + address.landmark + " , " + address.panchayat + " , " + address.dist + " , " + address.pin + " , " + al_number
    total_product = len(cart)
    for data in cart:
        total += float(data.product.discount_price) * float(data.customer_quantity)
    #id = Orderid.generate_id()

    if total <= 100:
        delivery_charge = 10
    elif total > 100 and total <= 200:
        delivery_charge = 15
    elif total > 200 and total <= 350:
        delivery_charge = 20
    elif total > 350 and total <= 500:
        delivery_charge = 25
    else:
        delivery_charge = 0

    final_price =  total + delivery_charge

    ordid = generate_id()
    id = ordid
    payment_mode = ''
    status = 'Shipping'

    data_dict = {
            'MID': 'rJXvah34753603915703',
            'ORDER_ID': str(ordid),
            'TXN_AMOUNT': str(final_price),
            'CUST_ID': request.user.email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'https://www.favshops.com/cart/handlerequest/',
            }
    param_dict = data_dict
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANTKEY)
    return param_dict


   # return redirect('cart_checkout')



def create_order(request,id,amount):
    
    final_price = amount
    orderid = id

    mnumber = request.user.mobile_number
    

    cart = Cart.objects.filter(mobile_number = mnumber).order_by('-add_time')
    address = Address.objects.filter(mobile_number = mnumber).first()
    al_number = ","
    if address.alternate_number:
        al_number = address.alternate_number
    full_name = address.full_name

    total_address = full_name + " , " + address.at + " , " + address.landmark + " , " + address.panchayat + " , " + address.dist + " , " + address.pin + " , " + al_number
    total_product = len(cart)

    id = orderid
    payment_mode = 'Paytm'
    status = 'Shipping'
    for item in cart:
        brand = ''
        if item.product.brand:
            brand = item.product.brand
        else:
            brand = 'favshops'
        order = Order(image=item.product.image,order_id=id,payment_mode=payment_mode,mobile_number = mnumber,name=item.product.product_name,brand=brand,quantity = item.product.quantity,price=item.product.discount_price,address=total_address,status=status,margin_price=item.product.margin_price,customer_quantity=item.customer_quantity)
        order.save()

    #for item in cart:
        #item.delete()

    #return id,final_price

    #return render(request,'paymentstatus.html',{'response': response_dict})


@csrf_exempt
def handlerequest(request):

    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANTKEY, checksum)

    if verify:
        if response_dict['RESPCODE'] == '01':
            #id,final_price = create_order(request,response_dict)
            id = response_dict['ORDERID']
            final_price = response_dict['TXNAMOUNT']

            order = Order.objects.filter(order_id = id).first()
            number = order.mobile_number
            cart = Cart.objects.filter(mobile_number = number).order_by('-add_time')
            for item in cart:
                item.delete()

            return render(request,'success_order.html',{'id':id,'total':final_price})
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request,'paymentstatus.html',{'response': response_dict})




def create_order_cod(request):
    mnumber = request.user.mobile_number
    total = 0.0
    delivery_charge = 0
    cart = Cart.objects.filter(mobile_number = mnumber).order_by('-add_time')
    address = Address.objects.filter(mobile_number = mnumber).first()
    al_number = ","
    if address.alternate_number:
        al_number = address.alternate_number
    full_name = address.full_name

    total_address = full_name + " , " + address.at + " , " + address.landmark + " , " + address.panchayat + " , " + address.dist + " , " + address.pin + " , " + al_number
    total_product = len(cart)
    for data in cart:
        total += float(data.product.discount_price) * float(data.customer_quantity)
    #id = Orderid.generate_id()

    if total <= 100:
            delivery_charge = 10
    elif total > 100 and total <= 200:
        delivery_charge = 15
    elif total > 200 and total <= 350:
        delivery_charge = 20
    elif total > 350 and total <= 500:
        delivery_charge = 25
    else:
        delivery_charge = 0

    final_price = delivery_charge + total

    ordid = generate_id()
    id = ordid
    payment_mode = 'COD'
    status = 'Shipping'
    for item in cart:
        brand = ''
        if item.product.brand:
            brand = item.product.brand
        else:
            brand = 'favshops'
        order = Order(image=item.product.image,order_id=id,payment_mode=payment_mode,mobile_number = mnumber,name=item.product.product_name,brand=brand,quantity = item.product.quantity,price=item.product.discount_price,address=total_address,status=status,margin_price=item.product.margin_price,customer_quantity=item.customer_quantity)
        order.save()

    for item in cart:
        item.delete()

    return id,final_price,total_address




def payment_mode(request):
    if request.method == 'POST':
        mode = request.POST['payment']
        if mode == 'cod':
            print('hi')
            id,total,address = create_order_cod(request)
            number = request.user.mobile_number
            subject = 'New Order Received'
            msg = "{0}   {1}   {2}    {3}".format(id,total,address,number)
            sender = 'officialfavshops@gmail.com'
            receiver = 'tarachandpattu@gmail.com'
            if id:
                send_mail(subject,msg,sender,[receiver],fail_silently=False)
                return render(request,'success_order.html',{'id':id,'total':total})

        elif mode == 'paytm':
            param_dict = create_order_paytm(request)
            final_price = param_dict['TXN_AMOUNT']
            orderid = param_dict['ORDER_ID']
            create_order(request,orderid,final_price)
            return render(request, 'paytm.html', {'param_dict': param_dict})

        else:
            print('hello')
            return redirect('cart_checkout')
    return redirect('index')

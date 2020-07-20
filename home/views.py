from django.shortcuts import render,redirect
from Products.forms import Product_form
from Products.models import Product
from django.contrib import messages
from cart.models import Cart
from order.models import Order

# Create your views here.

def index(request):
    special_offer = Product.objects.filter(special_offer=True).order_by('-upload_time')
    cartlen = 0
    cart = None
    if request.user.is_authenticated:
        mnumber = request.user.mobile_number
        cart = Cart.objects.filter(mobile_number = mnumber)
        cartlen = len(cart)
    grocery = Product.objects.filter(category='Grocery').order_by('-upload_time')
    snacks = Product.objects.filter(category='Snacks').order_by('-upload_time')
    masala = Product.objects.filter(category='Masala').order_by('-upload_time')

    return render(request,'index.html',{'special_offer':special_offer,'cartlen':cartlen,'cart':cart,'grocery':grocery,'snacks':snacks,'masala':masala})

def cart_page(request):
    mnumber = request.user.mobile_number
    total = 0.0
    cart = Cart.objects.filter(mobile_number = mnumber).order_by('-add_time')
    for data in cart:
        total += float(data.product.discount_price)
    return render(request,'cart.html',{'cart':cart,'total':total})

def user_register(request):
    return render(request,'register.html')

def user_login(request):
    return render(request,'login.html')

def wish_list(request):
    return render(request,'wishlist.html')

def forget_password(request):
    return render(request,'forget_password.html')

def admin_page(request):
    
    return redirect('all_products')

def about(request):
    return render(request,'about.html')

def order_history(request):
    mnumber = request.user.mobile_number
    orders = Order.objects.filter(mobile_number = mnumber).order_by('-order_date').filter(order_canceled=False)
    total = 0.0
    for ord in orders:
        total += float(ord.price)

    return render(request,'order_history.html',{'orders':orders,'total':total})

def contact(request):
    return render(request,'contact.html')

def profile_page(request):
    user = request.user
    return render(request,'profile.html')

def product_details(request,pk):
    prod = Product.objects.get(pk=pk)
    return render(request,'product_details.html',{'product':prod})

def delivery_boy(request):
    not_packed = Order.objects.filter(packed = False).order_by('order_id').filter(delivered=False).filter(order_canceled=False)
    not_delivered = Order.objects.filter(delivered=False)

    not_packed_ids = set([i.order_id for i in not_packed])
    sorted_not_packed_ids = sorted(not_packed_ids)
    #print(not_packed_ids)

    list = []
    dict = {}

    for id in sorted_not_packed_ids:
        list = []
        for j in not_packed:
            if j.order_id == id:
                list.append(j)
        dict[id] = list


    return render(request,'delivery_boy.html',{'not_packed':not_packed,'not_delivered':not_delivered,'not_packed_ids':not_packed_ids,'dict':dict})


def not_delivered(request):
    not_delivered = Order.objects.filter(delivered=False).filter(packed=True).order_by('order_id').filter(order_canceled = False)

    not_delivered_ids = set([i.order_id for i in not_delivered])
    sorted_not_delivered_ids = sorted(not_delivered_ids)

    list = []
    dict = {}
    total_price = 0.0
    dict_total = {}
    dict_address = {}
    delivery_charge = 0


    for id in sorted_not_delivered_ids:
        list = []
        total_price = 0.0
        delivery_charge = 0
        for j in not_delivered:
            if j.order_id == id:
                list.append(j)
                total_price += float(j.price)

        if total_price <= 100:
            delivery_charge = 10
        elif total_price > 100 and total_price <= 200:
            delivery_charge = 15
        elif total_price > 200 and total_price <= 350:
            delivery_charge = 20
        elif total_price > 350 and total_price <= 500:
            delivery_charge = 25
        else:
            delivery_charge = 0


        order = Order.objects.filter(order_id=id)[0]
        address = order.address
        contactno = order.mobile_number
        
        dict_address[id] = address


        final_price = delivery_charge + total_price
    
        price_address = [(final_price,address,contactno),]
        list.append(price_address)
        dict[id] = list
        dict_total[id] = final_price
        print(dict_address)

    return render(request,'not_delivered.html',{'dict':dict,'dict_total':dict_total,'dict_address':dict_address})

def order_packed(request,pk):
    order = Order.objects.get(pk=pk)
    order.packed = True
    order.status = 'Packed'
    order.save()
    return redirect('delivery_boy_page')

def big_sale(request):
    special_offer = Product.objects.filter(special_offer=True).order_by('-upload_time')
    best_offer = Product.objects.filter(best_offer=True).order_by('-upload_time')
    return render(request,'big_sale.html',{'special_offer':special_offer,'best_offer':best_offer})

def cooking_oil(request):
    cooking_oil = Product.objects.filter(category='Cooking oil').order_by('-upload_time')
    return render(request,'cooking_oil.html',{'cooking_oil':cooking_oil})

def beauty_products(request):
    beauty_products = Product.objects.filter(category='Beauty_products').order_by('-upload_time')
    return render(request,'beauty_products.html',{'beauty_products':beauty_products})
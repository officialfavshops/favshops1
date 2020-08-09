from django.shortcuts import render,redirect
from Products.forms import Product_form
from Products.models import Product
from django.contrib import messages
from cart.models import Cart
from order.models import Order
from User.models import User
from random import sample

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
    beauty_products = Product.objects.filter(category='Beauty_products').order_by('-upload_time')
    hair_oil = Product.objects.filter(category='Hair oil').order_by('-upload_time')
    cold_drinks = Product.objects.filter(category='Drinks').order_by('-upload_time')
    tea = Product.objects.filter(category='Tea').order_by('-upload_time')
    biscuts = Product.objects.filter(category='Biscuts').order_by('-upload_time')
    soap = Product.objects.filter(category='Soap').order_by('-upload_time')
    tooth_paste = Product.objects.filter(category='Tooth paste').order_by('-upload_time')
    sanitary = Product.objects.filter(category='sanitary').order_by('-upload_time')
    purfumes = Product.objects.filter(category='purfumes').order_by('-upload_time')
    powders = Product.objects.filter(category='powders').order_by('-upload_time')
    face_cream = Product.objects.filter(category='face_cream').order_by('-upload_time')
    detergent = Product.objects.filter(category='detergent').order_by('-upload_time')
    finail = Product.objects.filter(category='Finail').order_by('-upload_time')
    yeepi = Product.objects.filter(category='Yeepi noodles').order_by('-upload_time')

    return render(request,'index.html',{'special_offer':special_offer,'cartlen':cartlen,'cart':cart,'grocery':grocery,'snacks':snacks,'masala':masala,'beauty_products':beauty_products,'hair_oil':hair_oil,'cold_drinks':cold_drinks,'tea':tea,'biscuts':biscuts,'tooth_paste':tooth_paste,'soap':soap,'sanitary':sanitary,'purfumes':purfumes,'powders':powders,'face_cream':face_cream,'detergent':detergent,'finail':finail,'yeepi':yeepi})

def cart_page(request):
    mnumber = request.user.mobile_number
    total = 0.0
    cart = Cart.objects.filter(mobile_number = mnumber).order_by('-add_time')
    for data in cart:
        total += float(data.product.discount_price) * float(data.customer_quantity)
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
    products = list(Product.objects.all())
    related = list(sample(products,12))
    return render(request,'product_details.html',{'product':prod,'related':related})

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
                total_price += float(j.price) * float(j.customer_quantity)

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
        paid_status = ''
        if order.paid_status:
            paid_status = 'Paid'
        else:
            paid_status = 'Not Paid'

        price_address = [(final_price,address,contactno,paid_status),]
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

def masala(request):
    masala = Product.objects.filter(category='Masala').order_by('-upload_time')
    return render(request,'masala.html',{'masala':masala})

def grocery(request):
    grocery = Product.objects.filter(category='Grocery').order_by('-upload_time')
    return render(request,'grocery.html',{'grocery':grocery})

def cold_drinks(request):
    cold_drinks = Product.objects.filter(category='Drinks').order_by('-upload_time')
    return render(request,'cold_drinks.html',{'cold_drinks':cold_drinks})

def snacks(request):
    snacks = Product.objects.filter(category='Snacks').order_by('-upload_time')
    return render(request,'snacks.html',{'snacks':snacks})

def soap(request):
    soap = Product.objects.filter(category='Soap').order_by('-upload_time')
    return render(request,'soap.html',{'soap':soap})

def biscuts(request):
    biscuts = Product.objects.filter(category='Biscuts').order_by('-upload_time')
    return render(request,'biscuts.html',{'biscuts':biscuts})

def tooth_paste(request):
    tooth_paste = Product.objects.filter(category='Tooth paste').order_by('-upload_time')
    return render(request,'tooth_paste.html',{'tooth_paste':tooth_paste})

def tea(request):
    tea = Product.objects.filter(category='Tea').order_by('-upload_time')
    return render(request,'tea.html',{'tea':tea})

def yeepi(request):
    yeepi = Product.objects.filter(category='Yeepi noodles').order_by('-upload_time')
    return render(request,'yeepi.html',{'yeepi':yeepi})

def hair_oil(request):
    hair_oil = Product.objects.filter(category='Hair oil').order_by('-upload_time')
    return render(request,'hair_oil.html',{'hair_oil':hair_oil})

def finail(request):
    finail = Product.objects.filter(category='Finail').order_by('-upload_time')
    return render(request,'finail.html',{'finail':finail})

def detergent(request):
    detergent = Product.objects.filter(category='detergent').order_by('-upload_time')
    return render(request,'detergent.html',{'detergent':detergent})

def face_cream(request):
    face_cream = Product.objects.filter(category='Face Cream').order_by('-upload_time')
    return render(request,'face_cream.html',{'face_cream':face_cream})

def powders(request):
    powders = Product.objects.filter(category='powders').order_by('-upload_time')
    return render(request,'powders.html',{'powders':powders})

def purfumes(request):
    purfumes = Product.objects.filter(category='Purfumes').order_by('-upload_time')
    return render(request,'purfumes.html',{'purfumes':purfumes})

def sanitary(request):
    sanitary = Product.objects.filter(category='Sanitary napkins').order_by('-upload_time')
    return render(request,'sanitary.html',{'sanitary':sanitary})


def customers(request):
    user = User.objects.all().order_by('-date_of_join')
    total = len(user)
    return render(request,'customers.html',{'user':user,'total':total})

def search(request):
    products = Product.objects.all().order_by('-upload_time')
    return render(request,'search.html',{'products':products})


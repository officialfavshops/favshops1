from django.shortcuts import render,redirect,HttpResponse
from .models import Order,Admin_order_summary
from User.models import User
from datetime import datetime

# Create your views here.
def cancel_order(request,pk):
    order = Order.objects.get(pk=pk)
    order.order_canceled = True
    order.save()
    return redirect('order_history')

def delete_delivery_item(request,pk):
    order = Order.objects.get(pk=pk)
    order.order_canceled = True
    order.save()

    return redirect('not_delivered')

def delete_packed_item(request,pk):
    order = Order.objects.get(pk=pk)
    order.order_canceled = True
    order.save()

    return redirect('delivery_boy_page')

def order_delivered(request):
    if request.method == 'POST':
        ord_id = request.POST['id']
        price = request.POST['total_price']
        pay_mode = request.POST['paymode']

        confirm_order = ''
        cancel_order = ''
        mnumber = ''
        address=''
        order_time = ''
        delivered_time = datetime.now()

        co_orders = Order.objects.filter(order_id = ord_id).filter(order_canceled = False).filter(delivered=False)
        can_orders = Order.objects.filter(order_id = ord_id).filter(order_canceled = True).filter(delivered=False)
        order_margin_price = 0
        order_delivery_charges = 0

        for ord in co_orders:
            item = ord.name + " | " + ord.quantity + " | " + ord.price
            confirm_order += item + " , "
            order_margin_price += int(ord.margin_price)
            mnumber = ord.mobile_number
            address = ord.address
            order_time = ord.order_date
            ord.delivered = True
            ord.save()

        for ord in can_orders:
            item = ord.name + " | " + ord.quantity + " | " + ord.price
            cancel_order += item + " , "
            ord.delivered = True
            ord.save()

        if int(price) <= 100:
            order_delivery_charges = 10
        elif int(price) > 100 and int(price) <= 200:
            order_delivery_charges = 15
        elif int(price) > 200 and int(price) <= 350:
            order_delivery_charges = 20
        elif int(price) > 350 and int(price) <= 500:
            order_delivery_charges = 25
        else:
            order_delivery_charges = 0

        user = User.objects.get(mobile_number = mnumber)
        customer_fullname = user.first_name + " " + user.last_name
        delivered_by = request.user.first_name + " " + request.user.last_name
        summary = Admin_order_summary.objects.create(order_id = ord_id,order_items = confirm_order,cancel_items=cancel_order,total_price=price,payment_mode=pay_mode,order_address=address,order_by=user,delivered_by=delivered_by,order_time=order_time,delivered_time=delivered_time,total_margin=str(order_margin_price),delivery_charges=str(order_delivery_charges))
        summary.save()
        return redirect('not_delivered')
    else:
        return redirect('not_delivered')

def admin_order_summary(request):
    summary = Admin_order_summary.objects.all().order_by('-delivered_time')
    overall_delivery_charge = 0
    overall_margin = 0
    today_delivery_charge = 0
    today_margin = 0

    today = datetime.today()
    print(today)
    today_summary = Admin_order_summary.objects.filter(date = today)
    print('summary ',today_summary)
    for ord in today_summary:
        today_delivery_charge += int(ord.delivery_charges)
        today_margin += int(ord.total_margin)

    for ord in summary:
        overall_delivery_charge += int(ord.delivery_charges)
        overall_margin += int(ord.total_margin)
    return render(request,'order_summary.html',{'summary':summary,'overall_delivery_charge':overall_delivery_charge,'overall_margin':overall_margin,'today_delivery_charge':today_delivery_charge,'today_margin':today_margin})
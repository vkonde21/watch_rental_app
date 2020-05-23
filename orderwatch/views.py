from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from orderwatch.models import OrderWatch, Booking
from product.models import Product
import datetime
from django.contrib import messages

# Create your views here.
def index(request):
    print("working")
    return HttpResponse(request,"hello")

@login_required
def showorders(request, id):
    orders = OrderWatch.objects.filter(user = request.user)
    params = {}
    if(orders.count() == 0):
        msg = "You have not placed an order since 6 months"
    else:
        for o in orders:
            b = Booking.objects.filter(order = o)
            print(b)
            if(b.count() != 0):
                params[o] = b[0] #assumming one order has only 1 booking
        msg = ""
        
    return render(request, "orderwatch/showorders.html", {"orders":params})

def about(request):
    return render(request, "orderwatch/about.html")

@login_required
def orderdetails(request, id):
    order = OrderWatch.objects.filter(order_id = id)
    b = Booking.objects.filter(order = order[0])
    product = b[0].watch
    params = {}
    params["order"] = order[0]
    params["booking"] = b[0]
    return render(request, "orderwatch/orderdetails.html", params)

@login_required
def cancel_order(request, orderid):
    order = OrderWatch.objects.get(order_id=orderid)
    order_date = order.ordered_date
    print(order_date)
    current_date = datetime.datetime.now(datetime.timezone.utc)
    date_diff = current_date - order_date
    minutes_diff = date_diff.total_seconds() / 60.0
    print(minutes_diff)
    booking = Booking.objects.filter(order__order_id=orderid)
    if minutes_diff <= 30:
        for b in booking:
            product = b.watch
            pid = product.product_id
            books = Booking.objects.filter(watch = product, order__isnull = False)
            print(books)
            if(len(books) < product.original_qty):
                pro = Product.objects.get(product_id = pid)
                pro.qty = product.original_qty - len(books)
                pro.save()
            b.delete()       #delete all bookings of a particular order.Right now each order has only 1 booking
        order.delete()
        messages.add_message(request, messages.SUCCESS, 
                             'Your order is cancelled.')
        return redirect('/home')
    else:
        messages.add_message(request, messages.INFO,
                             'Sorry, it is too late to cancel this order.')
        return redirect(f"/orderdetails/{orderid}")

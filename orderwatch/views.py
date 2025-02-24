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
    orders = orders.order_by('-ordered_date')
    params = {}

    if(orders.count() == 0):
        msg = "You have not placed an order since 6 months"
    else:
        for o in orders:
            b = Booking.objects.filter(order = o)
            print(b)
            if(b.count() != 0):
                params[o] = b 
        msg = ""
        
    return render(request, "orderwatch/showorders.html", {"orders":params})

def about(request):
    return render(request, "orderwatch/about.html")

@login_required
def orderdetails(request, id):
    order = OrderWatch.objects.filter(order_id = id)
    b = Booking.objects.filter(order = order[0])
    #product = b[0].watch
    params = {}
    params["order"] = order[0]
    params["booking"] = b
    
    return render(request, "orderwatch/orderdetails.html", params)

@login_required
def cancel_order(request, orderid, bookingid):

    order = OrderWatch.objects.get(order_id=orderid)
    order_date = order.ordered_date
    #print(order_date)
    current_date = datetime.datetime.now(datetime.timezone.utc)
    date_diff = current_date - order_date
    minutes_diff = date_diff.total_seconds() / 60.0
    booking = Booking.objects.filter(booking_id = bookingid)
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
            
            b.status = "cancelled"
            b.save()
            order.amount = order.amount - b.total 
            order.save()
        messages.add_message(request, messages.SUCCESS, 
                             f'Your order for {b.watch.title} is cancelled.')
        return redirect('/home')
    else:
        messages.add_message(request, messages.INFO,
                             'Sorry, it is too late to cancel this order.')
        return redirect(f"/orderdetails/{orderid}")

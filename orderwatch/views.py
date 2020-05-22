from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from orderwatch.models import OrderWatch, Booking

# Create your views here.
def index(request):
    print("working")
    return HttpResponse(request,"hello")

@login_required
def showorders(request, id):
    orders = OrderWatch.objects.filter(user = request.user)
    #print(orders)
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
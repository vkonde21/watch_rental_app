from django.shortcuts import render, HttpResponse
from orderwatch.models import Booking
from product.models import Product
from datetime import datetime
# Create your views here.
from django.contrib.auth.decorators import user_passes_test


def updateqty(product):
    p = Booking.objects.filter(product = product)

#@staff_member_required  //this decorator can be also used
@user_passes_test(lambda u: u.is_superuser)
def deletebooking(request):
    todaydate = datetime.today().strftime('%Y-%m-%d')
    #booking = Booking.objects.filter(final_date__lte = todaydate).count()
    n = Booking.objects.filter(order__isnull = True).delete()
    p = Product.objects.all()
    for prod in p:
        b = Booking.objects.filter(
            product__product_id=prod.product_id, final_date__lte=todaydate).count()
        l = len(b)
        if(l < prod.original_qty):
            g = Product.objects.get(product_id = prod.product_id)
            g.qty = g.original_qty - l
            g.save()
    return HttpResponse("bookings deleted")


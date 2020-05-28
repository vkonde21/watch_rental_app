from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, OrderWatch, BookingCart
from product.models import Product
from orderwatch.models import Booking
from django.contrib import messages
import datetime
from loginsystem.settings import CURRENCY
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail

# Create your views here.
def check(pid, d, e):
    #d is start date and e is end date
    product = Product.objects.filter(product_id = pid)
    if(product[0].qty == 0):
        d = datetime.datetime.strptime(d, "%d %B %Y").date()
        e = datetime.datetime.strptime(e, "%d %B %Y").date()
        pre = Booking.objects.filter(watch=product[0], order__isnull=False, status = "placed")
        #exclude all bookings which are booked between desired period
        watches = Booking.objects.filter(watch=product[0], order__isnull=False, status = "placed").exclude(
            initial_date__gte=d, final_date__lte=e).exclude(initial_date__lte=e, final_date__gte=e).exclude(initial_date__lte=d, final_date__gte=e).exclude(initial_date__lte=d,final_date__gte=d )
        print(pre)
        print(watches)
        l = len(pre) - len(watches)
        print(l)
        if(l >= product[0].original_qty):
            return 0    #not available
        else:
            return 1

    else:
        return 1

@login_required
def showcart(request, id):
    #here id is user_id
    cart = Cart.objects.get(user = request.user)
    cart.save()
    params= {}
    params["products"] = cart.products.all()
    return render(request, "cart/showcart.html", params)


@login_required
def addtocart(request, product_id):
    
    cart = Cart.objects.get(user=request.user)
    p = Product.objects.get(product_id=product_id)
    if(p not in cart.products.all()):
        cart.products.add(p)
    else:
        messages.info(request, "This product is already in your cart")
    print("add", cart.products.all())
    return redirect(f"/showcart/{request.user.id}")


@login_required
def removecart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    p = Product.objects.get(product_id=product_id)
    cart.products.remove(p)
    return redirect(f"/showcart/{request.user.id}")

def checkavailability(request, product_id):
    params = {}
    cart = Cart.objects.get(user=request.user)
    params["products"] = cart.products.all()
    d = request.GET.get("datepickers" + str(product_id), "")
    e = request.GET.get("datepickerr" + str(product_id), "")
    r = 0
    #print("checkav", d)
    #print("checkav", e)
    product = Product.objects.filter(product_id = product_id)
    if(d == "" or e == "" or d == None or e == None):
        messages.error(request, "Please select dates in both fields")
        return redirect("/showcart/" + f"{request.user.id}")
    else:
        r = check(product_id, d, e)
        if(r == 0):
            messages.error(request, f"{product[0].title} not available between selected dates")
        else:
            messages.success(
                request, f"{product[0].title} available between selected dates")
            #params[str(product[0].product_id)] = {"d":d, "e":e}
            
    return render(request, "cart/showcart.html", params)


@login_required
def placeorder(request, bookid):
    params = {}
    if(request.method == "POST"):
        name = request.user.username
        amount = request.POST.get("amount", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        address = request.POST.get(
            "address1", "") + request.POST.get("address2", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zip_code = request.POST.get("zip_code", "")
        order = OrderWatch(user=request.user, amount=amount, address=address, city=city, state=state,
                           zip_code=zip_code, name=name, email=email)
        order.save()
        bookings = Booking.objects.filter(bcart__book_id = bookid)
        
        for b in bookings:
            n = Booking.objects.get(booking_id=b.booking_id)
            n.order = order
            n.status = "placed"
            n.save()
            p = Product.objects.get(product_id = b.watch.product_id)
            if(p.qty > 0):
                p.qty = p.qty - 1
                p.save()

        bookcart = BookingCart.objects.get(book_id=bookid)
        bookcart.ordercart = order
        bookcart.save()
        l = []
        l.append(request.user.email)
        html_message = render_to_string(
            'product/mail_template.html', {'order_id': order.order_id})
        plain_message = strip_tags(html_message)
        mail.send_mail(
            'order details', plain_message, 'pplwatch9@gmail.com', l, html_message=html_message)
        messages.success(request, "Your order has been placed successfully !!!Check your mail for further details")
        return redirect("/home")
    else:   
        params["bookid"] = bookid
        bookings = Booking.objects.filter(bcart__book_id=bookid)
        t = 0
        for b in bookings:
            n = Booking.objects.get(booking_id = b.booking_id)
            e = n.final_date
            d = n.initial_date
            days = (e - d).days
            n.days = days
            total = days * n.watch.final_value
            total = total + n.watch.deposit
            n.total = total
            t = t + total
            n.save()
        bookings = Booking.objects.filter(bcart__book_id=bookid)
        params["bookings"] = bookings
        params["currency"] = CURRENCY
        params["total"] = t
        #return render(request, "cart/placeorder.html", params)
        return params


@login_required
def checkorder(request):
    c = 0
    cart = Cart.objects.get(user = request.user)
    products = cart.products.all()
    for p in products:
        d = request.GET.get("datepickers" + str(p.product_id), "")
        e = request.GET.get("datepickerr" + str(p.product_id), "")
        #print("datepickers" + str(p.product_id))
        if(d == "" or e == ""):
            messages.error(request, "Please select return date as well as starting date for all products")
            return redirect(f"/showcart/{request.user.id}")
        r = check(p.product_id, d, e)
        if(r == 0):
            messages.error(
                request, f"{p.title} not available between selected dates")
            c = c + 1
    if(c == 0):
        bcart = BookingCart(user = request.user)
        bcart.save()
        bcartid = bcart.book_id
        for p in products:
            d = request.GET.get("datepickers" + str(p.product_id), "")
            e = request.GET.get("datepickerr" + str(p.product_id), "")
            d = datetime.datetime.strptime(d, "%d %B %Y").date()
            e = datetime.datetime.strptime(e, "%d %B %Y").date()
            b = Booking(watch=p, initial_date=d,
                        final_date=e, user=request.user, bcart = bcart)
            b.save()

        params = placeorder(request, bcartid)
        return render(request, "cart/placeorder.html", params)

    else:
        redirect(f"/showcart/{request.user.id}")
            



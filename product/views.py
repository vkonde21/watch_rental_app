from django.shortcuts import render, redirect, HttpResponse
from .models import Product, Category, Review
from orderwatch.models import Booking, OrderWatch
from math import ceil
from django.contrib import messages
from django.conf import settings
from . import Checksum
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from .forms import ReviewForm, ReviewUpdateForm
from django.views.generic import ListView, DetailView
# Create your views here.
import datetime 

b_id = 0
'''def checkbooking(bookid):
    b = Booking.objects.filter(booking_id = bookid)
    idate = b[0].initial_date
    fdate = b[0].final_date
    what if user does not logout for many days and places the order after the booking is already taken'''

# Function to covert string to datetime 
def convert(date_time): 
    format = '%d %b %Y' # The format 
    datetime_str = datetime.strptime(date_time, format).date()
    return datetime_str 

def is_valid_queryparam(param):
    return param != '' and param is not None

def search(request):
    qs = Product.objects.all()
    categories = Category.objects.all()
    title_contains_query = request.GET.get('title')
    minrent = request.GET.get('minrent')
    maxrent = request.GET.get('maxrent')
    date_min = request.GET.get('startdate')
    date_max = request.GET.get('returndate')
    category = request.GET.get('category')
    if(category == "Choose..."):
        category = ""
    if is_valid_queryparam(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)

    if(is_valid_queryparam(minrent)):
        qs = qs.filter(final_value__gte = minrent)
    
    if(is_valid_queryparam(maxrent)):
        qs = qs.filter(final_value__lte = maxrent)

    if(is_valid_queryparam(category)):
        c = Category.objects.filter(title = category)
        qs = qs.filter(category = c[0].id)
    
    if(is_valid_queryparam(date_min) and is_valid_queryparam(date_max)):
        date_min = datetime.datetime.strptime(date_min, "%d %B %Y").date()
        date_max = datetime.datetime.strptime(date_max, "%d %B %Y").date()
        q = qs.filter(qty__gte = 1)
        b = Booking.objects.exclude(
            initial_date__gte=date_min, final_date__lte=date_max).exclude(
            initial_date__lte = date_max, final_date__gte = date_max).exclude(initial_date__lte = date_min, final_date__gte= date_max)
        b1 = Booking.objects.filter(order__isnull = True)
        b = list(b)
        for x in b1:
            b.append(x)
        if(len(b) == 0):
            qs = list(q)
        else:
            qs = list(q)
            for book in b:
                if(book.watch not in qs):
                    qs.append(book.watch)

    elif(is_valid_queryparam(date_min)):
        messages.error(request, "Please select return date")
        redirect("/homepage")

    elif(is_valid_queryparam(date_max)):
        messages.error(request, "Please select start date")
        redirect("/homepage")

            
    
    params = {"queryset":qs}
    return render(request, "product/search.html", params)

def homepage(request):
    thanks = True
    products = Product.objects.all()
    allProds = []
    catprods = Product.objects.values("category", "product_id")
    cats = {item["category"] for item in catprods}
    categories = Category.objects.values("title")
    category = [c["title"] for c in categories]
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nslides), nslides])

    params = {"allProds": allProds, "cats":category}
    return render(request, "product/homepage.html", params)

def productview(request, id):
    #Fetch the product by its id
    prod = Product.objects.filter(product_id = id)
    return render (request, "product/productview.html", {"product": prod[0]})

def checkout(request):
    thank = False
    ido = 0
    product_id = request.GET.get("pname", "")
    CURRENCY = settings.CURRENCY
    if(request.user.is_authenticated):
        if(request.method == "POST"):
            name = request.POST.get("name", "")
            amount = request.POST.get("amount", "")
            email = request.POST.get("email", "")
            phone = request.POST.get("phone", "")
            address = request.POST.get("address1", "") + request.POST.get("address2", "")
            city = request.POST.get("city", "")
            state = request.POST.get("state", "")
            zip_code = request.POST.get("zip_code", "")
            order = OrderWatch(user = request.user, amount = amount, address = address, city = city, state = state, 
                                zip_code = zip_code, name = name, email = email)
            order.save()
            global b_id
            b = Booking.objects.get(booking_id = b_id)
            b.order = order
            b.save()
            l = []
            l.append(request.user.email)
            send_mail(
                'order details', f"Your order id is{order.order_id}",'kdprasad0036@gmail.com', l)
            MERCHANT_KEY = 'UV&5KgZ6DBavlics'
            param_dict = {
                'MID': 'xplqWT25914630031497',
                'ORDER_ID': str(ido),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
   	        'CALLBACK_URL': 'http://127.0.0.1:8000/product/handlerequest',
            }
        # The above code is taken from here:https://github.com/Paytm-Payments/Paytm_Web_Sample_Kit_Python/blob/master/pythonKit%203.X/test.cgi
            param_dict["CHECKSUMHASH"] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            
            return render(request, "product/paytm.html", {"param_dict":param_dict})
        else:
            d = request.GET.get("datepickers", "")
            e = request.GET.get("datepickerr", "")
            if(d == "" or e =="" or d==None or e == None):
                messages.error(request, "Please select dates in both fields")
                return redirect("/product/productview/" + f"{product_id}")
            product_id = request.GET.get("pname", "")
            product = Product.objects.filter(product_id = product_id)
            #print(product[0].qty)
            if(product[0].qty == 0):
                d = datetime.datetime.strptime(d, "%d %B %Y").date()
                e = datetime.datetime.strptime(e, "%d %B %Y").date()
                pre = Booking.objects.filter(watch = product[0])
                watches = Booking.objects.filter(watch = product[0]).exclude(
                initial_date__gte=d, final_date__lte=e).exclude(initial_date__lte = e, final_date__gte = e).exclude(initial_date__lte = d, final_date__gte= e)
                w1 = Booking.objects.filter(order__isnull = True)
                watches = list(watches)
                for x in w1:
                    watches.append(x)
                print(watches)
                l = len(pre) - len(watches)
                #if all quantities of watch between that period are booked then
                if(l >= product[0].original_qty or len(watches) == 0):
                    messages.error(request, "Not available between selected dates!!")
                    return redirect("/product/productview/" + f"{product_id}")
                
                else:
                    print(watches[0].initial_date)
                    print(watches[0].final_date)
                    b = Booking(watch = product[0], initial_date = d, final_date = e, user = request.user)
                    b.save()
                    b_id = b.booking_id
                p = product[0]
            else:
                d = datetime.datetime.strptime(d, "%d %B %Y").date()
                e = datetime.datetime.strptime(e, "%d %B %Y").date()
                p = Product.objects.get(product_id = product_id)
                q = p.qty - 1
                p.qty = q
                p.save()
                b = Booking(watch = p, initial_date = d, final_date = e, user = request.user)
                b.save()
                b_id = b.booking_id
            days = (e - d).days
            total = days * p.final_value
            
        return render (request, "product/checkout.html",{"thank":thank,"id":ido, "product":p,"days":days, "total":f'{CURRENCY} {total}',"initial_date":d, "final_date":e, "amount":total})
    else:
        messages.info(request, "You need to login")
        return redirect("/product/productview/"+f"{product_id}")


@csrf_exempt
def handlerequest(request):
    #pay tm will send you a post request here
    #To check if payment is done or not
    return HttpResponse("done")


def review(request, id):
    k = 0
    if(request.method == "POST"):
        #while saving the form 
        
        try:
            r = Review.objects.get(
                        user=request.user, product__product_id=id)

            if(r is not None):
                form = ReviewUpdateForm(instance=r, data=request.POST)
                a = form.save(commit=False)
                k = 1
        except:
            pass
        if( k == 0):
            form = ReviewForm(request.POST)
            a = form.save(commit=False)
        a.user = request.user
        a.product = Product.objects.get(product_id = id)
        a.save()
        return redirect("/product/productview/" + f"{id}")
    else:
        if(request.user.is_authenticated):
            b = Booking.objects.filter(watch__product_id = id, user = request.user, order__isnull = False)
            
            if(len(b) == 0):
                messages.error(request, "You cannot write a review since u have not rented this")
                return redirect("/product/productview/"+f"{id}")

            else:
                review = ReviewForm()
                #in case user has already written a review update the review
                try:
                    r = Review.objects.get(
                        user=request.user, product__product_id=id)
                
                    if(r is not None):
                        review = ReviewUpdateForm(instance = r)
                except:
                    pass
                
            return render(request, "product/review.html", {"product_id":id, "form":review})
        else:
            messages.info(request, "Please Log in to write a review")
            return redirect("/product/productview/"+f"{id}")

def showreview(request, id):
    reviews = Review.objects.filter(product__product_id = id)
    #print(reviews)
    if(len(reviews) == 0):
        messages.info(request, "No reviews for this product till date")   
        return redirect("/product/productview/"+f"{id}")
    else:
        return render(request, "product/showreview.html", {"id":id, "reviews":reviews})
    

'''class ReviewListView(ListView):
    #<app>/<model>_<viewtype>.html
    model = Review 
    template_name = "product/showreview.html"
    context_object_name = 'reviews'
    ordering = ['-date_posted'] #- for newest to oldest

class ReviewDetailView(DetailView):
    model = Review'''
    

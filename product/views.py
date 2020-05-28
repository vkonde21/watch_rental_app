from django.shortcuts import render, redirect, HttpResponse
from .models import Product, Category, Review
from orderwatch.models import Booking
from cart.models import OrderWatch
from math import ceil
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import ReviewForm, ReviewUpdateForm
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import date
from django.contrib.auth.decorators import login_required

# Create your views here.
import datetime 
import json

b_id = 0

# Function to covert string to datetime 
def convert(date_time): 
    format = '%d %b %Y' # The format 
    datetime_str = datetime.strptime(date_time, format).date()
    return datetime_str 

def is_valid_queryparam(param):
    return param != '' and param is not None

def update(id):
    prod = Product.objects.get(product_id=id)
    reviews = Review.objects.filter(product__product_id=id)
    c = reviews.count()
    r = [0, 1, 2, 3, 4, 5]
    s = 0
    if(c != 0):
        for k in reviews:
            s = s + k.rating
        average = round(s/c, 2)
        prod.rating = average
        prod.save()

def search(request):
    qs = Product.objects.all()
    categories = Category.objects.all()
    title_contains_query = request.GET.get('title')
    minrent = request.GET.get('minrent')
    maxrent = request.GET.get('maxrent')
    d_min = request.GET.get('startdate')
    d_max = request.GET.get('returndate')
    cate = request.GET.get('category')
    rating = request.GET.get('rate')
    qs = Product.objects.all()
    #print(type(rating))
    if(cate == "Choose..."):
        cate = ""

    if(rating == "Choose Rating..."):
        rating = ""
    if is_valid_queryparam(title_contains_query):
        qs = qs.filter(Q(title__icontains=title_contains_query) | Q(description__icontains = title_contains_query))
        

    if(is_valid_queryparam(minrent)):
        qs = qs.filter(final_value__gte = minrent)
    
    if(is_valid_queryparam(maxrent)):
        qs = qs.filter(final_value__lte = maxrent)

    
    if(is_valid_queryparam(cate)):
        c = Category.objects.filter(title = cate)
        if(c is not None):
            qs = qs.filter(category = c[0].id)

    if(is_valid_queryparam(rating)):
        qs = qs.filter(rating__gte = rating)
    
    if(is_valid_queryparam(d_min) and is_valid_queryparam(d_max)):
        date_min = datetime.datetime.strptime(d_min, "%d %B %Y").date()
        date_max = datetime.datetime.strptime(d_max, "%d %B %Y").date()
        #for every product in qs find whether it is available between the chosen dates
        for p in qs:
            pre = Booking.objects.filter(watch = p, order__isnull = False, status ="placed")
            b = Booking.objects.filter(watch=p, order__isnull = False, status = "placed").exclude(
                initial_date__gte=date_min, final_date__lte=date_max).exclude(
                initial_date__lte=date_max, final_date__gte=date_max).exclude(initial_date__lte=date_min, final_date__gte=date_max).exclude(initial_date__lte=date_min, final_date__gte=date_min)
            l = pre.count() - b.count()
            if(l >= p.original_qty):
                qs = qs.exclude(product_id = p.product_id)
        #print(qs)
    elif(is_valid_queryparam(d_min)):
        messages.error(request, "Please select return date")
        redirect("/homepage")

    elif(is_valid_queryparam(d_max)):
        messages.error(request, "Please select start date")
        redirect("/homepage")
    
    catprods = Product.objects.values("category", "product_id")
    cats = {item["category"] for item in catprods}
    categories = Category.objects.values("title")
    category = [c["title"] for c in categories]
    params = {"cats": category,
              "queryset": qs, "search": 1}
    params["title"] = title_contains_query
    params["minrent"] = minrent
    params["maxrent"] = maxrent
    params["startdate"] = d_min
    params["returndate"] = d_max
    params["cate"] = cate
    params["rating"] = rating
    prods = {}
    if(len(qs) == 0):
        params["pmessage"] = "Sorry, no search results found for your query"
    else:
        cats = Category.objects.all()
        ids = []
        for l in qs:
            ids.append(l.product_id)
        qs = Product.objects.filter(product_id__in = ids)
        for cat in cats:
            q = qs.filter(category = cat)
            if(q.count() != 0):
                prods[cat.title] = q
        #print(prods)
    params["prods"] = prods
    params["currency"] = settings.CURRENCY
    return render(request, "product/homepage.html", params)

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

    params = {"allProds": allProds, "cats":category, "search":0, "currency":settings.CURRENCY}
    return render(request, "product/homepage.html", params)

def productview(request, id):
    #Fetch the product by its id
    prod = Product.objects.filter(product_id = id)
    reviews = Review.objects.filter(product__product_id=id)
    c = reviews.count()
    r = [0, 1, 2, 3, 4, 5]
    params = {}
    s = 0
    for v in r:
        q = reviews.filter(rating=v)
        params["r" + str(v)] = q.count()
        s = s + q.count() * v
    params["product"] = prod[0]
    if(c == 0):
        params["rmessage"] = "No reviews for this product yet"
        params["average"] = 0
        params["totalr"] = 0
    else:
        params["rmessage"] = ""
        params["average"] = round(s / c, 1)
        params["totalr"] = c
    params["currency"] = settings.CURRENCY
    return render (request, "product/productview.html", params)

@login_required
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
            b.status = "placed"
            b.save()
            p = Product.objects.get(product_id = b.watch.product_id)
            if(p.qty > 0):
                q = p.qty - 1
                p.qty = q
                p.save()
            l = []
            l.append(request.user.email)
            html_message = render_to_string(
                'product/mail_template.html', {'order_id': order.order_id})
            plain_message = strip_tags(html_message)
            mail.send_mail(
                'order details', plain_message, 'pplwatch9@gmail.com', l, html_message=html_message)
            
            messages.success(request, "Order placed successfully.Check your email for further details")
            return redirect("/home")
            
        else:
            d = request.GET.get("datepickers", "")
            e = request.GET.get("datepickerr", "")
            if(d == "" or e =="" or d==None or e == None):
                messages.error(request, "Please select dates in both fields")
                return redirect("/product/productview/" + f"{product_id}")
            product_id = request.GET.get("pname", "")
            product = Product.objects.filter(product_id = product_id)
            if(product[0].qty == 0):
                d = datetime.datetime.strptime(d, "%d %B %Y").date()
                e = datetime.datetime.strptime(e, "%d %B %Y").date()
                pre = Booking.objects.filter(watch = product[0], order__isnull = False, status = "placed")
                #exclude all bookings which are booked between desired period
                watches = Booking.objects.filter(watch = product[0], order__isnull = False, status="placed").exclude(
                    initial_date__gte=d, final_date__lte=e).exclude(initial_date__lte=e, final_date__gte=e).exclude(initial_date__lte=d, final_date__gte=e).exclude(initial_date__lte=d, final_date__gte=d)
                print(watches)
                l = len(pre) - len(watches)
                #if all quantities of watch between that period are booked then
                if(l == product[0].original_qty):
                    messages.error(request, "Not available between selected dates!!")
                    return redirect("/product/productview/" + f"{product_id}")
                
                else:
                    b = Booking(watch = product[0], initial_date = d, final_date = e, user = request.user)
                    b.save()
                    b_id = b.booking_id
                    print(b_id)
                p = product[0]
            else:
                d = datetime.datetime.strptime(d, "%d %B %Y").date()
                e = datetime.datetime.strptime(e, "%d %B %Y").date()
                p = Product.objects.get(product_id = product_id)
                b = Booking(watch = p, initial_date = d, final_date = e, user = request.user)
                b.save()
                b_id = b.booking_id
                print(b_id)
            days = (e - d).days
            total = days * p.final_value
            total = total + p.deposit
            b.total = total
            b.days = days
            b.save()
        return render (request, "product/checkout.html",{"thank":thank,"id":ido, "product":p,"days":days, "total":f'{CURRENCY} {total}',"initial_date":d, "final_date":e, "amount":total})
    else:
        messages.info(request, "You need to login")
        return redirect("/product/productview/"+f"{product_id}")



def review(request, id):
    k = 0
    current_date = date.today()
    if(request.method == "POST"):
        #while saving the form 
        try:
            r = Review.objects.get(
                        user=request.user, product__product_id=id)
            if(r is not None):
                form = ReviewUpdateForm(request.POST, request.FILES, instance = r)
                a = form.save(commit=False)
                k = 1
        except:
            pass
        if( k == 0):
            form = ReviewForm(request.POST, request.FILES)
            a = form.save(commit=False)
        a.user = request.user
        a.product = Product.objects.get(product_id = id)
        a.save()
        #Update product.rating which is the average rating
        update(id)
        return redirect("/product/productview/" + f"{id}")
    else:
        if(request.user.is_authenticated):
            b = Booking.objects.filter(watch__product_id = id, user = request.user, order__isnull = False)
            b = b.filter(Q(status = 'placed') | Q(status = 'delivered') | Q(status = 'refund'))
            if(len(b) == 0):
                messages.error(request, "You cannot write a review since you have not rented this")
                return redirect("/product/productview/"+f"{id}")

            else:
                #book = b.filter(initial_date__gte = current_date)
                #if(len(book) > 0):
                review = ReviewForm()
                #in case user has already written a review update the review
                try:
                    r = Review.objects.get(
                        user=request.user, product__product_id=id)
                
                    if(r is not None):
                        review = ReviewUpdateForm(instance = r)
                except:
                    pass

                #else:
                    #messages.error(
                        #request, "You cannot write a review since you have been delivered this yet")
                    #return redirect("/product/productview/"+f"{id}")
                    
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
    

def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Product.objects.filter(Q(title__startswith=q) |Q(description__icontains = q))
        results = []
        print (q)
        for r in search_qs:
            results.append(r.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
    

from django.shortcuts import render
from . import Checksum
# Create your views here.
def shipping(request):
    thank = False
    ido = 0
    if(request.method == "POST"):
        name = request.POST.get("name", "")
        amount = request.POST.get("amount", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        address = request.POST.get("address1", "") + request.POST.get("address2", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zip_code = request.POST.get("zip_code", "")
        MERCHANT_KEY = 'UV&5KgZ6DBavlics'
        
        return render(request, "order/paytm.html", {"param_dict": param_dict})
        #add payment url here

    else:
        title = request.GET.get("title")
        final_value = request.GET.get("finalvalue")
        days = request.GET.get("days")
        total = request.GET.get("total")
        initial_date = request.GET.get("intialdate")
        final_date = request.GET.get("finaldate")
        print(title, final_value, days, total, initial_date, final_date)
    return render(request, "order/shipping.html")

from django.shortcuts import render, HttpResponse
from orderwatch.models import Booking
from datetime import datetime
# Create your views here.
from django.contrib.auth.decorators import user_passes_test

#@staff_member_required  //this decorator can be also used
@user_passes_test(lambda u: u.is_superuser)
def deletebooking(request):
    todaydate = datetime.today().strftime('%Y-%m-%d')
    booking = Booking.objects.filter(final_date__lte = todaydate).delete()
    print(booking)
    return HttpResponse("bookings deleted")

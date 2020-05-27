from django.db import models
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils import timezone
from product.models import Product
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib.auth.models import UserManager
from cart.models import Cart, BookingCart, OrderWatch
CURRENCY = settings.CURRENCY



class Booking(models.Model):
    #if we get an order whose rental date clashes with the other order then change the availablity
    #status of watch availability
    '''On the item's model, add two datetime fields, for example "bookedStart"
     and "bookedEnd". And have a function isBooked() that checks if a given datetime or the current datetime is in 
    that time frame, and return True if it is, or False otherwise.'''
    watch = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="booking")
    initial_date = models.DateField()
    final_date = models.DateField()
    days = models.PositiveIntegerField(default = 0)
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderWatch, on_delete=models.CASCADE, null=True)
    bcart = models.ForeignKey(BookingCart, on_delete = models.CASCADE, null = True)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2) #total here refers to amount fr each booking betw chosen dates
    status = models.CharField(max_length = 12, default="noorder")
    #no order means no order has been placed for a booking
    #cancelled means booking cancelled
    #delivered means booking has been done and delivered & return date is over
    #placed means order has been placed
    

    

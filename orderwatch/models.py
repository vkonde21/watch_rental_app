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
CURRENCY = settings.CURRENCY


class OrderWatch(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(default=timezone.now())
    order_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=0)  
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=300) 
    state = models.CharField(max_length=90)
    city = models.CharField(max_length=90)
    zip_code = models.CharField(max_length=90)
    objects = UserManager()
    def __str__(self):
        return self.user.username


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
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderWatch, on_delete=models.CASCADE, null=True)
    objects = UserManager()
    

    

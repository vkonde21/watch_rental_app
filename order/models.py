from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils import timezone
from product.models import Product
from django.contrib.auth.models import User
from product.models import Booking

from decimal import Decimal
CURRENCY = settings.CURRENCY


'''class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"'''


class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(default = timezone.now())
    order_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=300)
    state = models.CharField(max_length=90)
    city = models.CharField(max_length=90)
    zip_code = models.CharField(max_length=90)
    


    def __str__(self):
        return self.user.username

    

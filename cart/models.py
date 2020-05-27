from django.db import models
from django.contrib.auth.models  import User
from product.models import Product
from django.utils import timezone

# Create your models here.


'''#OrderCart is same as OrderWatch but user places an order via cart
class OrderCart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(default=timezone.now())
    order_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=300)
    state = models.CharField(max_length=90)
    city = models.CharField(max_length=90)
    zip_code = models.CharField(max_length=90)

    def __str__(self):
        return self.user.username'''


class OrderWatch(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(default=timezone.now())
    order_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    name = models.CharField(max_length=90, default ="")
    email = models.CharField(max_length=90)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=300)
    state = models.CharField(max_length=90)
    city = models.CharField(max_length=90)
    zip_code = models.CharField(max_length=90)

    def __str__(self):
        return self.user.username



class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True, null=True)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)


class BookingCart(models.Model):
    book_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    ordered_date = models.DateTimeField(default=timezone.now())
    ordercart = models.ForeignKey(
        OrderWatch, on_delete=models.PROTECT, null=True)

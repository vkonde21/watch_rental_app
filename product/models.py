from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings
from .managers import ProductManager
from order.models import Order
CURRENCY = settings.CURRENCY




class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    #c_id = models.AutoField(primary_key = True)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    product_id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL)
    subcategory = models.CharField( max_length=50, default = "Men")
    description = models.CharField(max_length=400, default = "")
    active = models.BooleanField(default=True)
    value = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    discount_value = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=10)
    deposit = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    final_value = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=10)
    qty = models.PositiveIntegerField(default=0)
    original_qty = models.PositiveIntegerField(default = 0)
    pub_date = models.DateField()
    objects = models.Manager()
    browser = ProductManager()
    image = models.ImageField(upload_to="product_pics", default="default.jpg")
    
    class Meta:
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        self.final_value = self.discount_value if self.discount_value > 0 else self.value

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def tag_final_value(self):
        return f'{self.final_value} {CURRENCY}'

    def update(self, qty):
        self.qty = qty
    tag_final_value.short_description = 'Value'

class Booking(models.Model):
    #if we get an order whose rental date clashes with the other order then change the availablity
    #status of watch availability
    '''On the item's model, add two datetime fields, for example "bookedStart"
     and "bookedEnd". And have a function isBooked() that checks if a given datetime or the current datetime is in 
    that time frame, and return True if it is, or False otherwise.'''
    watch = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "booking")
    initial_date = models.DateField()
    final_date = models.DateField()
    booking_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    
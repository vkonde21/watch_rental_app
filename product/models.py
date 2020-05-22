from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings
from .managers import ProductManager
from django.utils import timezone
CURRENCY = settings.CURRENCY



class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
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
    image = models.ImageField(upload_to="product_pics", default="default.jpg")
    rating = models.DecimalField(max_digits = 3, default = 0.00, decimal_places = 2)
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

class Review(models.Model):
    RATING_CHOICES = ((0,'0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to = "review_pics")
    rating = models.IntegerField(choices=RATING_CHOICES, default = 0)
    content = models.TextField(max_length = 6000)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    date_posted = models.DateField(default = timezone.now())
    review_id = models.AutoField(primary_key = True)
    
    
'''class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    review = models.ForeignKey(Review, on_delete = models.CASCADE)
    comment = models.TextField(max_length = 120)
    cdate = models.DateField(default = timezone.now())'''
    

from django.db import models

# Create your models here.
from django.conf import settings
from .managers import ProductManager

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
    description = models.CharField(max_length=400, default = "")
    active = models.BooleanField(default=True)
    value = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    discount_value = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=10)
    final_value = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=10)
    qty = models.PositiveIntegerField(default=0)
    pub_date = models.DateField()
    objects = models.Manager()
    browser = ProductManager()
    

    class Meta:
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        self.final_value = self.discount_value if self.discount_value > 0 else self.value
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def tag_final_value(self):
        return f'{self.final_value} {CURRENCY}'
    tag_final_value.short_description = 'Value'

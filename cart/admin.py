from django.contrib import admin
from .models import Cart, OrderWatch, BookingCart
# Register your models here.
admin.site.register(Cart)
admin.site.register(OrderWatch)
admin.site.register(BookingCart)
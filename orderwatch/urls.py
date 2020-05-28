from django.urls import path
from .views import index, showorders, about, orderdetails, cancel_order

urlpatterns = [
    path("index", index, name="index"), 
    path("orders/<int:id>", showorders, name="showorders"),
    path("about", about, name="about"),
    path("orderdetails/<int:id>", orderdetails, name="orderdetails"),
    path("cancel_order/<int:orderid>/<int:bookingid>", cancel_order, name="cancel_order")
]

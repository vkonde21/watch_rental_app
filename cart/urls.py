from django.urls import path, include
from .views import showcart, addtocart, removecart,checkavailability, checkorder, placeorder
urlpatterns=[
    path("showcart/<int:id>", showcart, name="showcart"),
    path("addtocart/<int:product_id>", addtocart, name="addtocart"),
    path("check/<int:product_id>", checkavailability, name="check"),
    path("checkorder", checkorder, name="checkorder"),
    path("placeorder/<int:bookid>", placeorder, name="placeorder"),
    path("removecart/<int:product_id>", removecart, name="removecart")
    ]
from django.urls import path, include
from .views import shipping

urlpatterns = [
    path("shipping", shipping, name = "shipping")
]
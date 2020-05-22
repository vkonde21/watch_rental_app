from django.urls import path
from .views import index, showorders, about

urlpatterns = [
    path("index", index, name="index"), 
    path("orders/<int:id>", showorders, name="showorders"),
    path("about", about, name="about")
]

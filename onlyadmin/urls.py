from .views import deletebooking
from django.urls import path, include
urlpatterns = [path("deletebook", deletebooking, name="delete"),]

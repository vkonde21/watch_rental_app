from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def index(request):
    print("working")
    return HttpResponse(request,"hello")
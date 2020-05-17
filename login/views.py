from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from orderwatch.models import Booking
from django.contrib.auth import logout
# Create your views here.
def register(request):
    form = UserRegisterForm()
    if(request.method == "POST"):
        form = UserRegisterForm(request.POST)
        #print(form)
        if(form.is_valid()):
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            print(password)
            messages.success(request, f"Account created for {username} !!")
            form.save()
            return redirect("/login")

    return render(request, 'login/register.html',{"form":form})
    
def basic(request):
    return render(request, "login/basic.html")

@login_required
def profile(request):
    if(request.method == "POST"):
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        u_name = request.POST.get("username")
        print(u_name)
        print(request.user.username)
        if(u_form.is_valid() and p_form.is_valid()):
            #
            if(u_name != request.user.username):
                p = User.objects.filter(u_name)
                if(len(p) > 0):
                    messages.error(request, "Username already exists")
                    return redirect("/profile")
            u_form.save()
            p_form.save()
            messages.success(request, "Profile Updated!!")
            return redirect("/profile")

    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
    context = {"p_form":p_form, "u_form":u_form}
    return render(request,'login/profile.html',context)

def logout1(request):
    #print(request.user)
    try:
        #It might happen that a customer books a watch but does not place an order.
        #In that case the booking gets deleted when the customer logs out
        b = Booking.objects.get(user=request.user, order__isnull = True)
        #print(b)
        if(b is not None):
            b.delete()
    except:
        pass
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/home")


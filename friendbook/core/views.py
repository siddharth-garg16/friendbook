import re
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required(login_url='signin')
def index(request):
    return render(request, "index.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "This email is already taken.")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "This username is already taken.")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                #creating profile object for the new user
                user_model = User.objects.get(username)
                new_profile = User.objects.create_user(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.info(request, "Passwords didn't match.")
            return redirect('signup')
    else:
        return render(request, "signup.html")

def signin(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid credentials")
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

def setting(request):
    pass
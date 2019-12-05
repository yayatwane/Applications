from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
# Create your views here.


def index(request):
    return render(request, 'register.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        print(first_name)
        print(last_name)
        print(username)
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print('Username taken')
                messages.info(request, 'Username taken')
                return render(request, 'register.html')
            elif User.objects.filter(email=email).exists():
                print('Email taken')
                messages.info(request, 'Email taken')
                return render(request, 'register.html')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print('User created')
                messages.info(request, 'User Created')
                return render(request, 'register.html')
    else:
        return render(request, 'register.html')
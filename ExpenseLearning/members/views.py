from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        print("AUTH USER:", user)  # 🔥 DEBUG LINE

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'members/login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')
    
import re

from django.contrib import auth
from django.db import IntegrityError
from django.shortcuts import render, redirect

from weigo.models import MyUser


def landing(request):
    if request.user.is_authenticated:
        return redirect('/profile.html')
    return redirect('/login.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('/profile.html')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        info = MyUser.objects.filter(email=email).first()
        if info is None:
            return render(request, 'login.html', {'login_error': 'email not found.'})
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('/profile.html')
        else:
            return render(request, 'login.html', {'login_error': 'password is invalid.'})

    return render(request, 'login.html')


def registration(request):
    if request.user.is_authenticated:
        return redirect('/profile.html')
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        email_valid = r'^[0-9a-zA-Z\_\-]+(\.[0-9a-zA-Z\_\-]+)*@[0-9a-zA-Z]+(\.[0-9a-zA-Z]+){1,}$'
        if not re.match(email_valid, email):
            return render(request, 'registration.html', {'registration_error': 'enter a valid email address.'})
        username_valid = r'^[a-z]+$'
        if not re.match(username_valid, username):
            return render(request, 'registration.html', {'registration_error': 'username has illegal characters.'})
        if len(password) < 6:
            return render(request, 'registration.html', {'registration_error': 'password too short.'})
        if password != password_confirmation:
            return render(request, 'registration.html', {'registration_error': 'password mismatch.'})

        try:
            MyUser.objects.create_user(email=email, username=username, password=password)
        except IntegrityError:
            return render(request, 'registration.html', {'registration_error': 'email already taken.'})
        '''except Exception:
            return render(request, 'registration.html', {'registration_error': 'username already taken.'})'''
        return redirect('/login.html')
    return render(request, 'registration.html')


def profile(request):
    if request.user.is_authenticated:
        info = MyUser.objects.filter(email=request.user.email).first()
        return render(request, 'profile.html', {'email': info.email,
                                                'username': info.username,
                                                'password': info.password})
    return redirect('/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/login.html')

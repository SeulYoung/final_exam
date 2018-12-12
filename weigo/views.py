import re
from django.contrib import auth
from django.shortcuts import render, redirect
from django.db.models import Q, F
from django.contrib.auth.backends import ModelBackend
from django.views.decorators.csrf import csrf_protect

from weigo import models
from weigo.models import MyUser, WeiboData

data_list = [
    {'author': "jack", "content": "abc", "postData": "aaa"}
]


class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = MyUser.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def landing(request):
    if request.user.is_authenticated:
        return redirect('/profile.html')
    return render(request, 'index.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('/profile.html')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        info = MyUser.objects.filter(Q(email=email) | Q(username=email)).first()
        if info is None:
            return render(request, 'login.html', {'login_error': 'email not found.'})
        user = auth.authenticate(username=email, password=password)
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

        info = MyUser.objects.filter(email=email).first()
        if info is not None:
            return render(request, 'registration.html', {'registration_error': 'email already taken.'})
        info = MyUser.objects.filter(username=username).first()
        if info is not None:
            return render(request, 'registration.html', {'registration_error': 'username already taken.'})
        MyUser.objects.create_user(email=email, username=username, password=password)

        return redirect('/login.html')
    return render(request, 'registration.html')


@csrf_protect
def dynamic(request):
    if request.method == "POST":
        author = request.POST.get('author')
        content = request.POST.get('content')
        likes = 0
        WeiboData.objects.create(author=author, content=content, likes=likes)
        data_list = models.WeiboData.objects.all().order_by('-postData')
        return render(request, 'circle.html', {'data': data_list})

    info = MyUser.objects.filter(email=request.user.email).first()
    return render(request, 'dynamic.html', {'email': info.email, 'username': info.username})


def myDynamic(request):
    data_list = models.WeiboData.objects.filter(author=request.user.username).order_by('-postData')
    info = MyUser.objects.filter(email=request.user.email).first()
    return render(request, 'myDynamic.html', {'data': data_list})


def circle(request):
    if request.method == "POST":
        author = request.POST.get('author')
        postData = request.POST.get('postData')
        likes = request.POST.get('likes')
        WeiboData.objects.filter(Q(author=author) & Q(postData=postData)).update(likes=F('likes') + 1)

    data_list = models.WeiboData.objects.all().order_by('-postData')
    return render(request, 'circle.html', {'data': data_list})


def profile(request):
    if request.user.is_authenticated:
        info = MyUser.objects.filter(email=request.user.email).first()
        return render(request, 'profile.html', {'email': info.email, 'username': info.username})
    return redirect('/login.html')


def email_update(request):
    if request.method == "POST":
        email = request.POST.get('email')
        email_valid = r'^[0-9a-zA-Z\_\-]+(\.[0-9a-zA-Z\_\-]+)*@[0-9a-zA-Z]+(\.[0-9a-zA-Z]+){1,}$'

        if not re.match(email_valid, email):
            return render(request, 'emailUpdate.html', {'email_error': 'enter a valid email address.'})
        info = MyUser.objects.filter(email=email).first()
        if info is not None:
            return render(request, 'emailUpdate.html', {'email_error': 'email already taken.'})
        MyUser.objects.filter(email=request.user.email).update(email=email)
        return redirect('/login.html')

    return render(request, 'emailUpdate.html')


def password_update(request):
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        if not request.user.check_password(old_password):
            return render(request, 'passwordUpdate.html', {'password_error': 'invalid password.'})
        if len(password) < 6:
            return render(request, 'passwordUpdate.html', {'password_error': 'password too short.'})
        if password != password_confirmation:
            return render(request, 'passwordUpdate.html', {'password_error': 'password mismatch.'})
        request.user.set_password(password)
        request.user.save()
        return redirect('/login.html')

    return render(request, 'passwordUpdate.html')


def logout(request):
    auth.logout(request)
    return redirect('landing')

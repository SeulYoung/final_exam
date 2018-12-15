from django.contrib import auth
from django.shortcuts import render, redirect
from django.db.models import Q, F
from django.contrib.auth.backends import ModelBackend
from django.views.decorators.csrf import csrf_protect

from weigo import models
from weigo.forms import *
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
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('/profile.html')
            else:
                form.add_error('password', 'Password is invalid.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def registration(request):
    if request.user.is_authenticated:
        return redirect('/profile.html')
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            MyUser.objects.create_user(email=email, username=username, password=password)
            return redirect('/login.html')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


@csrf_protect
def dynamic(request):
    if not request.user.is_authenticated:
        return redirect('/login.html')
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
    if not request.user.is_authenticated:
        return redirect('/login.html')
    data_list = models.WeiboData.objects.filter(author=request.user.username).order_by('-postData')
    info = MyUser.objects.filter(email=request.user.email).first()
    return render(request, 'myDynamic.html', {'data': data_list})


def circle(request):
    if not request.user.is_authenticated:
        return redirect('/login.html')
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
    if not request.user.is_authenticated:
        return redirect('/login.html')
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            MyUser.objects.filter(email=request.user.email).update(email=email)
            return redirect('/login.html')
    else:
        form = RegistrationForm()
    return render(request, 'emailUpdate.html', {'form': form})


def password_update(request):
    if not request.user.is_authenticated:
        return redirect('/login.html')
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            password = form.cleaned_data['password2']

            if request.user.check_password(old_password):
                request.user.set_password(password)
                request.user.save()
                return redirect('/login.html')
            else:
                form.add_error('password', 'Invalid password.')
    else:
        form = RegistrationForm()
    return render(request, 'PasswordUpdate.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('landing')

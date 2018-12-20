from django.contrib import auth
from django.shortcuts import render, redirect
from django.db.models import F
from django.contrib.auth.backends import ModelBackend
from django.views.decorators.csrf import csrf_protect

from weigo import models
from weigo.forms import *


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
        return redirect('/profile')
    return render(request, 'index.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('/profile')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('/profile')
            else:
                form.add_error('password', 'Password is invalid.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def registration(request):
    if request.user.is_authenticated:
        return redirect('/profile')
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            MyUser.objects.create_user(email=email, username=username, password=password)
            return redirect('/login')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


@csrf_protect
def dynamic(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == "POST":
        author = request.POST.get('author')
        content = request.POST.get('content')
        if 'private' in request.POST:
            models.WeiboData.objects.create(author=author, content=content, private=True)
        else:
            models.WeiboData.objects.create(author=author, content=content)
        data_list = models.WeiboData.objects.filter(private=False).order_by('-postData')
        data = []
        for k in data_list:
            temp = k.__dict__
            temp['judge'] = 0
            temp['follow'] = 0
            judge = models.WeiboLike.objects.filter(Q(num=k.num) & Q(liker=request.user.username))
            follow = models.Follow.objects.filter(Q(author=k.author) & Q(follower=request.user.username))
            if judge:
                temp['judge'] = 1
            if follow:
                temp['follow'] = 1
            data.append(temp)
        return render(request, 'circle.html', {'data': data, 'username': request.user.username})

    info = MyUser.objects.filter(email=request.user.email).first()
    return render(request, 'dynamic.html', {'email': info.email, 'username': info.username})


def myDynamic(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == "POST":
        num = request.POST.get('num')
        models.WeiboData.objects.filter(num=num).delete()
        models.WeiboLike.objects.filter(num=num).delete()
    data_list = models.WeiboData.objects.filter(author=request.user.username).order_by('-postData')
    return render(request, 'myDynamic.html', {'data': data_list})


def circle(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == "POST":
        if 'like' in request.POST:
            num = request.POST.get('num')
            result = models.WeiboLike.objects.get_or_create(num=num, liker=request.user.username)
            if result[1]:
                models.WeiboData.objects.filter(num=num).update(likes=F('likes') + 1)
            else:
                result[0].delete()
                models.WeiboData.objects.filter(num=num).update(likes=F('likes') - 1)
        elif 'follow' in request.POST:
            author = request.POST.get('author')
            result = models.Follow.objects.get_or_create(author=author, follower=request.user.username)
            if not result[1]:
                result[0].delete()
        elif 'delete' in request.POST:
            num = request.POST.get('num')
            models.WeiboData.objects.filter(num=num).delete()
            models.WeiboLike.objects.filter(num=num).delete()

    data_list = models.WeiboData.objects.filter(private=False).order_by('-postData')
    data = []
    for k in data_list:
        temp = k.__dict__
        temp['judge'] = 0
        temp['follow'] = 0
        judge = models.WeiboLike.objects.filter(Q(num=k.num) & Q(liker=request.user.username))
        follow = models.Follow.objects.filter(Q(author=k.author) & Q(follower=request.user.username))
        if judge:
            temp['judge'] = 1
        if follow:
            temp['follow'] = 1
        data.append(temp)
    return render(request, 'circle.html', {'data': data, 'username': request.user.username})


def follower(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    data_list = models.Follow.objects.filter(author=request.user.username)
    return render(request, 'following.html', {'data': data_list})


def following(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'POST':
        if 'like' in request.POST:
            num = request.POST.get('num')
            result = models.WeiboLike.objects.get_or_create(num=num, liker=request.user.username)
            if result[1]:
                models.WeiboData.objects.filter(num=num).update(likes=F('likes') + 1)
            else:
                result[0].delete()
                models.WeiboData.objects.filter(num=num).update(likes=F('likes') - 1)
        elif 'follow' in request.POST:
            author = request.POST.get('author')
            models.Follow.objects.filter(author=author, follower=request.user.username).delete()

    follow_list = models.Follow.objects.filter(follower=request.user.username)
    data = []
    for f in follow_list:
        data_list = models.WeiboData.objects.filter(author=f.author, private=False).order_by('-postData')
        for k in data_list:
            temp = k.__dict__
            temp['judge'] = 0
            judge = models.WeiboLike.objects.filter(Q(num=k.num) & Q(liker=request.user.username))
            if judge:
                temp['judge'] = 1
            data.append(temp)

    return render(request, 'following.html', {'follow_list': follow_list, 'data': data})


def profile(request):
    if request.user.is_authenticated:
        info = MyUser.objects.filter(email=request.user.email).first()
        return render(request, 'profile.html', {'email': info.email, 'username': info.username})

    return redirect('/login')


def email_update(request):
    if not request.user.is_authenticated:
        return redirect('/login')
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
        return redirect('/login')
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            password = form.cleaned_data['password']

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

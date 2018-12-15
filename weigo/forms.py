import re

from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

from weigo.models import MyUser


def email_check(email):
    pattern = re.compile(r'^[0-9a-z\-_]+(\.[0-9a-z\-_]+)*@[0-9a-z]+(\.[0-9a-z]+)+$')
    return re.match(pattern, email)


def username_check(username):
    pattern = re.compile(r'^[a-z0-9\-_]+$')
    return re.match(pattern, username)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password1 = forms.CharField(label='Password1', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            filter_result = User.objects.filter(email=email)
            if len(filter_result) > 0:
                raise forms.ValidationError('Email already taken.')
        else:
            raise forms.ValidationError('Enter a valid email address.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 50:
            raise forms.ValidationError('Username too long.')
        if username_check(username):
            filter_result = User.objects.filter(username=username)
            if len(filter_result) > 0:
                raise forms.ValidationError('Username already taken.')
        else:
            raise forms.ValidationError('Username has illegal characters.')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError('Password too short.')
        elif len(password1) > 50:
            raise forms.ValidationError('Password too long.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password mismatch.')
        return password2


class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_email(self):
        username = self.cleaned_data.get('email')
        filter_result = MyUser.objects.filter(Q(email=username) | Q(username=username)).first()
        if not filter_result:
            raise forms.ValidationError('User not found.')
        return username


class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            filter_result = User.objects.filter(email=email)
            if len(filter_result) > 0:
                raise forms.ValidationError('Email already taken.')
        else:
            raise forms.ValidationError('Enter a valid email address.')
        return email


class PasswordForm(forms.Form):
    old_password = forms.CharField(label='OldPassword', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Password1', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError('Password too short.')
        elif len(password1) > 50:
            raise forms.ValidationError('Password too long.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password mismatch.')
        return password2

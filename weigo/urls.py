from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login.html/', views.login, name='login'),
    path('registration.html/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('profile.html/', views.profile, name='profile'),
    path('emailUpdate.html/', views.email_update, name='email_update'),
    path('passwordUpdate.html/', views.password_update, name='password_update'),
    path('dynamic.html/', views.dynamic, name='dynamic'),
    path('myDynamic.html/', views.myDynamic, name='myDynamic'),
    path('circle.html/', views.circle, name='circle'),
]

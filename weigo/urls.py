from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login.html/', views.login, name='login'),
    path('registration.html/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('profile.html/', views.profile, name='profile'),
]

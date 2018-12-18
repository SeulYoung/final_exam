from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('emailUpdate/', views.email_update, name='email_update'),
    path('passwordUpdate/', views.password_update, name='password_update'),
    path('dynamic/', views.dynamic, name='dynamic'),
    path('myDynamic/', views.myDynamic, name='myDynamic'),
    path('circle/', views.circle, name='circle'),
    path('follow/', views.follower, name='follow'),
]

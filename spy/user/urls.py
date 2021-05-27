from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django import views as django_views
from .views import HitmanCreate, HitmenDetailUpdate, HitmenList, LoginView, LogoutView


app_name = 'user'

urlpatterns = [
    path('', LoginView.as_view(success_url='hits/'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', HitmanCreate.as_view(), name='register'),
    path('hitmen/', login_required(HitmenList.as_view()), name='hitmen_list'),
    path('hitmen/<int:pk>/', login_required(HitmenDetailUpdate.as_view()), name='hitmen_detail'),
]
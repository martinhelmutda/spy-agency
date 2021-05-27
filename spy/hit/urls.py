from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django import views as django_views
from .views import HitBulkEdit, HitCreate, HitDetailUpdate, HitsList


app_name = 'hit'

urlpatterns = [
    path('', login_required(HitsList.as_view()), name='hits_list'),
    path('<int:pk>/', login_required(HitDetailUpdate.as_view()), name='hit_detail'),
    path('create/', login_required(HitCreate.as_view()), name='hit_create'),
    path('bulk/', login_required(HitBulkEdit.as_view()), name='hit_bulk_edit'),
]
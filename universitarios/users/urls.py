from django.urls import path, include
from django.conf.urls import include, url
from . import views
import dashboard.views

app_name = 'users'

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('registrar/', views.ProfileCreate.as_view(), name='register_profile'),
]
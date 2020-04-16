from django.urls import path, include
from django.conf.urls import include, url
from . import views
import users.urls
import dashboard.urls
import dashboard.views
app_name = 'core'

urlpatterns = [
    path(   '',views.HomePageView.as_view(),name = 'Home'),

]
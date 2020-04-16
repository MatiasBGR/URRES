from django.urls import path, include
from django.conf.urls import include, url
from . import views
import users.urls
import core.urls

app_name = 'dashboard'
urlpatterns = [
    path('adm/', views.adm.as_view(), name='adm'),
    path('socio/', views.socio, name='socio'),
    path('content/', views.load_content, name='load_content'),
]
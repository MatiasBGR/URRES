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
    path('position/', views.add_position_ok, name='add_position_ok'),
    path('record/', views.add_record_ok, name='add_record_ok'),
    path('player/', views.add_player_ok, name='add_player_ok'),
    path('match/', views.add_match_ok, name='add_match_ok'),
    path('training/', views.add_training_ok, name='add_training_ok'),
    path('measure/', views.add_measure_ok, name='add_measure_ok'),
    path('Assistance/', views.mark_assistance_ok, name='mark_assistance_ok'),
    path('Minute/', views.mark_assistance_ok, name='add_minute_ok'),

]
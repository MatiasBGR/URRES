from django.shortcuts import render
from users.models import Profile
from core.models import Minute, Isue
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.generic import  TemplateView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from functools import partial


# Create your views here.
class adm(TemplateView):
    template_name = "home2.html"
def socio(request):
    is_partner = request.user.groups.filter(name__in=['socio']).exists()
    is_player = request.user.groups.filter(name__in=['jugador']).exists()
    is_directive = request.user.groups.filter(name__in=['directiva']).exists()

    if is_directive: 
        return render(request, 'dashboard.html',context)
    if is_player:
        return render(request, 'dashboard.html')
    if is_partner:
        minutes = Minute.objects.all()
        isues = Isue.objects.all()
        return render(request, 'dashboard2.html',{'minutes':minutes,'isues':isues})

@csrf_protect       
def load_content(request):
    if request.POST and request.is_ajax:
        data = request.POST['click_id']
        response_data = type_of_request(data)
        return HttpResponse(response_data)

def get_minute(ids):
    minute = Minute.objects.get(id=ids)
    return render_to_string("content/minute.html",{'minute': minute })
def get_isue(ids):
    isue = Isue.objects.get(id=ids)
    return render_to_string("content/isue.html",{'isue': isue })
def get_register(ids):
    isue = Isue.objects.get(id=ids)
    return render_to_string("content/register-all.html",{'isue': isue })
def add_register(ids):
    return render_to_string("content/register.html",{})
def add_position(ids):
    return render_to_string("content/new_position.html",{})
def type_of_request(messaje):
    action = ""
    action = messaje.split('|')[0]
    ids = messaje.split('|')[1]
    switcher = {
        'get_isue': get_isue,
        'get_minute': get_minute,
        'get_register': get_register,
        'add_register': add_register,
        'add_position':add_position
    }
    return switcher[action](ids)
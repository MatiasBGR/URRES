import simplejson as simplejson
from datetime import datetime as dt
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from django.views.generic import  TemplateView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.loader import render_to_string
from functools import partial
from django.template import RequestContext
from users.models import Profile
from core.models import Minute, Isue
from dashboard.models import Position, Player, Match, Training, Assistants
from dashboard.forms import PositionForm, PlayerForm, RecordForm, MatchForm, TrainingForm, MeasureForm, AssistanceForm
from django.contrib import messages 
from django.contrib.auth.models import Group


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
        minutes = Minute.objects.all()
        isues = Isue.objects.all()
        exist = hasattr(request.user, 'player')
        return render(request, 'dashboard2.html',{'minutes':minutes,'isues':isues,'exist':exist})
    if is_partner:
        minutes = Minute.objects.all()
        isues = Isue.objects.all()
        return render(request, 'dashboard2.html',{'minutes':minutes,'isues':isues})

@csrf_protect       
def load_content(request):
    if request.POST and request.is_ajax:
        data = request.POST['click_id']
        response_data = type_of_request(data,request)
        return HttpResponse(response_data)

def get_minute(ids,request):
    minute = Minute.objects.get(id=ids)
    return render_to_string("content/minute.html",{'minute': minute })
def get_isue(ids,request):
    isue = Isue.objects.get(id=ids)
    return render_to_string("content/isue.html",{'isue': isue })
def get_register(ids,request):
    isue = Isue.objects.get(id=ids)
    return render_to_string("content/register-all.html",{'isue': isue })
def add_register(ids,request):
    return render_to_string("content/register.html",{})
def add_position(CreateView,request):
    template_name = "content/new_position.html"
    form_class = PositionForm
    def get_success_url(self):
        return reverse('dashboard:socio')
    return render_to_string("content/new_position.html",{'form':form_class},request)
def add_player(CreateView,request):
    template_name = "content/new_player.html"
    form_class = PlayerForm
    exist = hasattr(request.user, 'player')
    def get_success_url(self):
        return reverse('dashboard:socio')
    return render_to_string("content/new_player.html",{'form':form_class,'exist':exist},request)
def add_record(CreateView,request):
    template_name = "content/new_record.html"
    form_class = RecordForm
    def get_success_url(self):
        return reverse('dashboard:socio')
    return render_to_string("content/new_record.html",{'form':form_class},request)
def add_measure(CreateView,request):
    template_name = "content/new_measure.html"
    form_class = MeasureForm
    def get_success_url(self):
        return reverse('dashboard:socio')
    return render_to_string("content/new_measure.html",{'form':form_class},request)
def add_match(CreateView,request):
    template_name = "content/new_match.html"
    form_class = MatchForm
    options = Match.objects.values_list('opponent', flat=True)
    def get_success_url(self):
        return reverse('dashboard:socio')
    return render_to_string("content/new_match.html",{'form':form_class,'options':options},request)
def add_training(CreateView,request):
    template_name = "content/new_training.html"
    form_class = TrainingForm
    def get_success_url(self):
        return reverse('dashboard:socio')
    return render_to_string("content/new_training.html",{'form':form_class},request)
def see_training(ids,request):
    trainings = Training.objects.all()
    return render_to_string("content/see_training.html",{'trainings': trainings })
def mark_assistance(CreateView,request):
    last_training = Training.objects.filter(date__lte=dt.today()).order_by('-date').first()
    template_name = "content/mark_assistance.html"
    form_class = AssistanceForm(initial={'player': request.user.player, 'training': last_training})
    def get_success_url(self):
        return reverse('dashboard:socio')
    return render_to_string("content/mark_assistance.html",{'form':form_class},request)

def type_of_request(messaje,request):
    action = ""
    action = messaje.split('|')[0]
    ids = messaje.split('|')[1]
    switcher = {
        'get_isue': get_isue,
        'get_minute': get_minute,
        'get_register': get_register,
        'add_record': add_record,
        'add_measure': add_measure,
        'add_position':add_position,
        'add_player':add_player,
        'add_match':add_match,
        'add_training':add_training,
        'see_training':see_training,
        'mark_assistance':mark_assistance,
    }
    return switcher[action](ids,request)

def add_position_ok(request): 
    context = RequestContext(request)
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('dashboard:socio'))
    return HttpResponseRedirect(reverse('dashboard:socio'))
def add_training_ok(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('dashboard:socio'))
    error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
    return HttpResponse(simplejson.dumps(error_string))
def add_match_ok(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('dashboard:socio'))
        error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
        return HttpResponse(simplejson.dumps(error_string))
def add_measure_ok(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = MeasureForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.player = request.user.player
            obj.save()
            return HttpResponseRedirect(reverse('dashboard:socio'))
        error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
        return HttpResponse(simplejson.dumps(error_string))
def add_record_ok(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('dashboard:socio'))
    return HttpResponseRedirect(reverse('dashboard:socio'))
def add_player_ok(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            obj, created = Player.objects.update_or_create(
                user=request.user,
                defaults=form.cleaned_data
            )
            if created:
                my_group = Group.objects.get(name='jugador') 
                my_group.user_set.add(request.user)
                return HttpResponse(simplejson.dumps('Exito, ha sido creado como jugador'))
            if not created :
                return HttpResponse(simplejson.dumps('Exito, sus datatos fueron actualizados'))
        error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
        return HttpResponse(simplejson.dumps(error_string))
def mark_assistance_ok(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = AssistanceForm(request.POST)
        if form.is_valid():
            obj, created = Assistants.objects.update_or_create(
                player=request.user.player,
                training = Training.objects.filter(date__lte=dt.today()).order_by('-date').first(),
                defaults = {"observation":form.cleaned_data.get('observation')}
            )
            if created:
                return HttpResponse(simplejson.dumps('Exito, ha sido marcado como asistente'))
            if not created :
                return HttpResponse(simplejson.dumps('Exito, sus datatos fueron actualizados'))
        error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
        return HttpResponse(simplejson.dumps(error_string))
    
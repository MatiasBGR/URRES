from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
import dashboard.urls
from .models import Profile
from django import forms


# Create your views here.

def user_login(request):
	username = password = ''
	response_data = {}
	if request.POST and request.is_ajax:
		username = request.POST['username']
		password = request.POST['password']
		try:
			get_user = User.objects.get(username=username)
			if get_user.check_password(password):
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						try :
							user.profile 
							response_data = {'login' : "Success"}
						except:
							response_data = {'login' : "SuccessNoProfile"}
			else:
				response_data = {'user':"password wrong"}
		except User.DoesNotExist:
			response_data = {'user':"nouser"}
	else:
		username = password = ''
		response_data = {'login': "Failed"}
	return HttpResponse(JsonResponse(response_data))
	return redirect('users:profile')

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('avatar','rut', 'phone','birth_date') 
		widgets = {
			'avatar': forms.FileInput(attrs={'class': 'myfieldclass','id':'imageUpload'}),
			'rut': forms.TextInput(attrs={'class': 'myfieldclass'}),
			'phone': forms.TextInput(attrs={'class': 'myfieldclass'}),
			'birth_date': forms.DateInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker1','id': 'data_input'})
		}
class ProfileCreate(CreateView):
	template_name = "profile_form.html"
	form_class = ProfileForm
	def form_valid(self, form):
		print(form.errors)
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.incorporation_date = datetime.now()
		self.object.save()  
		return super(ProfileCreate, self).form_valid(form)
	def get_success_url(self):
		return reverse('dashboard:socio')

def set_field_html_name(cls, new_name):
    old_render = cls.widget.render
    def _widget_render_wrapper(name, value, attrs=None):
        return old_render(new_name, value, attrs)

    cls.widget.render = _widget_render_wrapper
@login_required
def index(request):
    group = request.user.groups.filter(user=request.user)[0]
    if group.name=="jugador":
        return HttpResponseRedirect(reverse('worker'))
    elif group.name=="socio":
        return HttpResponseRedirect(reverse('teamLeader'))
    elif group.name=="admin":
        return HttpResponseRedirect(reverse('adm'))

    context = {}
    template = "index.html"
    return render(request, template, context)
from .models import Profile
from django import forms

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

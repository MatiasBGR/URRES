from django import forms
from .models import Minute



class MinuteForm(forms.ModelForm):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
		label='Fecha',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',
			'style': 'font-size: 20px'
        })
    )
    class Meta:
        model = Minute
        fields = (
			'table',
			'date',
			'location',
            'locationGPS',
			'content',
		)
        labels = {
            'table':"Tabla:",
            'date':"Fecha:",
            'location':"Lugar:",
            'locationGPS': 'Lugar de reunión',
            'content':"Contenido:",
        }
        widgets = {
            'table': forms.TextInput(attrs={'id': 'observation','style': 'font-size: 20px','class': 'mdc-text-field__input w-100'}),
            'table': forms.TextInput(attrs={'id': 'observation','style': 'font-size: 20px','class': 'mdc-text-field__input w-100'}),
            'location': forms.TextInput(attrs={'id': 'place','style': 'font-size: 20px','class': 'mdc-text-field__input w-100'}),
        }
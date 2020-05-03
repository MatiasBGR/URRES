from .models import Player, Position, Record, Match, Training
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from mapwidgets.widgets import GooglePointFieldWidget
from bootstrap_datepicker_plus import DatePickerInput


class PlayerForm(forms.ModelForm):

	#e_phone = PhoneNumberField(required=True)
	emergency_phone = PhoneNumberField(
						widget=forms.TextInput(attrs={'placeholder':'+569123456789'}), 
                       	label="Número de emergencia", required=False,
					   	error_messages = {"invalid": 
						   "Numero ingresado incorrecto, debe ser de la forma : +56912345678"}
						)
	class Meta:
		model = Player
		fields = (
			'height',
			'weight',
			'position_one',
			'position_two',
			'years_played',
			'medical_conditions',
			'healthcare',
			)
		labels = {
			'height':"Altura en cm",
			'weight':"Peso en Kg",
			'position_one':"Primera Posición",
			'position_two':"Segunda Posición",
			'years_played': "Años jugados",
			'medical_conditions':"Condiciones medicas",
			'healthcare':"Seguro de salud, Fonasa o Clinica y cual ",
		}
		widgets = {
			'height': forms.NumberInput(attrs={'class': 'mdc-text-field__input w-100 form-control','id':'height','type':'number'}),
			'weight': forms.NumberInput(attrs={'class': 'mdc-text-field__input w-100 form-control','id':'weigth','type':'number'}),
			'position_one': forms.Select(attrs={'class': 'float-right btn btn-secondary dropdown-toggle w-100 form-control'}),
			'position_two': forms.Select(attrs={'class': 'float-right btn btn-secondary dropdown-toggle w-100 form-control'}),
			'years_played': forms.NumberInput(attrs={'class': 'mdc-text-field__input'}),
			'medical_conditions': forms.TextInput(attrs={'class': 'myfieldclass w-100'}),
			'healthcare': forms.TextInput(attrs={'class': 'mdc-text-field__input w-100'}),
		}
class PositionForm(forms.ModelForm):
	class Meta:
		model = Position
		fields = (
			'name',
			'number',
		)
		labels = {
			'name':"Nombre",
			'number':"Número",
		}
		widgets = {
			'name': forms.TextInput(attrs={'id': 'name','name': 'name','class':'mdc-text-field__input'}),
			'number': forms.TextInput(attrs={'id': 'number','name': 'number','class':'mdc-text-field__input'}),
		}
class RecordForm(forms.ModelForm):
	class Meta:
		model = Record
		fields = (
			'name',
			'description',
			'measure_unit',
			'info',
		)
		labels = {
			'name':"Nombre del registro",
			'description':"Descripción",
			'measure_unit':"Unidad de medida",
			'info':"Información Extra",
		}
		widgets = {
			'name': forms.TextInput(attrs={'id': 'name','name': 'title','class': 'mdc-text-field__input'}),
			'description': forms.TextInput(attrs={'description': 'title','name': 'title','class': 'mdc-text-field__input'}),
			'measure_unit': forms.TextInput(attrs={'measure_unit': 'title','name': 'title','class': 'mdc-text-field__input'}),
			'info': forms.TextInput(attrs={'id': 'info','name': 'title','class': 'mdc-text-field__input'}),
		}
class MatchForm(forms.ModelForm):
	TRUE_FALSE_CHOICES = (
    	(True, 'Sí'),
    	(False, 'No')
	)
	players = forms.ModelMultipleChoiceField(
			label='Jugadores',
            widget=forms.CheckboxSelectMultiple,
			queryset=Player.objects.all(),
            required=True)
	winnig = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="¿Ganamos?", 
                              initial='', widget=forms.Select(
								  attrs={'class': 'dropdown-toggle w-100 form-control'}), 
								  required=True)
	class Meta:
		model = Match
		fields = (
			'opponent',
			'points_infavor',
			'points_against',
			'winnig',
			'observation',
			'date',
			'duration',
			'players',
		)
		labels = {
			'opponent':'Rival',
			'points_infavor':'Puntos a Favor',
			'points_against':'Puntos en Contra',
			'winnig':'Ganamos',
			'observation':'Observaciónes',
			'date':'Fecha',
			'duration':'Duración',
			'players':'Jugadores',
		}
		widgets = {
			'opponent': forms.TextInput(attrs={'id': 'opponent','style': 'font-size: 20px','class': 'mdc-text-field__input'}),
			'points_infavor': forms.NumberInput(attrs={'id': 'points_infavor','style': 'font-size: 20px','class': ' mdc-text-field__input'}),
			'points_against': forms.NumberInput(attrs={'id': 'points_against','style': 'font-size: 20px','class': ' mdc-text-field__input'}),
			'observation': forms.TextInput(attrs={'id': 'observation','style': 'font-size: 20px','class': 'mdc-text-field__input'}),
			'date': forms.DateInput(attrs={'id': 'date','style': 'font-size: 20px','class': 'mdc-text-field__input'}),
			'duration': forms.TimeInput(attrs={'id': 'duration','style': 'font-size: 20px','class': 'mdc-text-field__input '}),
		}

class TrainingForm(forms.ModelForm):
	players = forms.ModelMultipleChoiceField(
			label='Jugadores participantes del entrenamiento',
            widget=forms.CheckboxSelectMultiple(
				attrs={ 'class':'btn btn-primary',
				'style': 'font-size: 20px'}),
			queryset=Player.objects.all(),
            required=False)
	date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',
			'style': 'font-size: 20px'
        })
    )
	class Meta:
		model = Training
		fields = (
			'observation',
			'place',
			'date',
			'players',
			'location',
		)
		labels = {
			'observation':"Comentario",
			'place':"Lugar",
			'date':'Fecha',
			'location': 'Lugar de entrenamiento'
		}
		widgets = {
			'observation': forms.TextInput(attrs={'id': 'observation','style': 'font-size: 20px','class': 'mdc-text-field__input'}),
			'place': forms.TextInput(attrs={'id': 'place','style': 'font-size: 20px','class': 'mdc-text-field__input'}),
		}
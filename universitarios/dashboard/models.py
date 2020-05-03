from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from mapbox_location_field.models import LocationField
from mapbox_location_field.spatial.models import SpatialLocationField
import datetime

# Create your models here.
class Position(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name = 'Posicion'
        verbose_name_plural = 'Posiciones'
    def __str__(self):
        return self.name
    
class Record(models.Model):
   name = models.CharField(max_length=100)
   description = models.TextField()
   measure_unit = models.CharField(max_length=100,blank=True)
   info = models.TextField(blank=True)
   class Meta:
       verbose_name = 'Registro'
       verbose_name_plural = 'Registros'
   def __str__(self):
        return self.name
 
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True,null=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    position_one = models.ForeignKey(Position,null=True, on_delete=models.SET_NULL,)
    position_two = models.ForeignKey(Position,null=True, on_delete=models.SET_NULL,related_name='%(class)s_requests_created') 
    years_played = models.PositiveIntegerField(null=True, blank=True)
    medical_conditions =  models.TextField(blank=True)
    healthcare   = models.CharField(max_length=300)
    emergency_phone  = PhoneNumberField(null=True, blank=True,region='CL')
    records = models.ManyToManyField(Record, through='Measure')
    class Meta:
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'
    def __str__(self):
        if hasattr(self.user, 'first_name'):
            return self.user.first_name
        return "No Name"

class Measure(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE,)
    record = models.ForeignKey(Record, on_delete=models.CASCADE,)
    measure= models.DecimalField(max_digits=5, decimal_places=3)
    date = models.DateTimeField(default=datetime.datetime.now)
    observation = models.TextField()
    class Meta:
        verbose_name = 'Asistentes a entrenamineto'
        verbose_name_plural = 'Asistentes a entrenaminetos'
    def __str__(self):
        return str(self.player.name+" "+self.record.name)

class Match (models.Model):
    opponent =  models.CharField(max_length=100)
    points_infavor = models.IntegerField(null=True, blank=True)
    points_against = models.IntegerField(null=True, blank=True)
    winnig = models.BooleanField(null=True)
    observation =  models.TextField()
    date  = models.DateField(null=True, blank=True)
    duration  = models.TimeField(null=True, blank=True)
    players = models.ManyToManyField(Player, through='Played')
    class Meta:
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'
    def __str__(self):
        return str(self.opponent)+" "+str(self.date)

class Played(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE,)
    match = models.ForeignKey(Match, on_delete=models.CASCADE,)
    start_duration  = models.TimeField(null=True, blank=True)
    end_duration  = models.TimeField(null=True, blank=True)
    observation = models.TextField()
    class Meta:
        verbose_name = 'Partido Jugado'
        verbose_name_plural = 'Partidos Jugados'
    def __str__(self):
        return str(self.player.user.first_name)+" "+str(self.player.user.last_name)+", "+str(self.match)
class Training(models.Model):
    observation =  models.TextField()
    place= models.CharField(max_length=250)
    date  = models.DateField(null=True, blank=True)
    location = LocationField(null=True, blank=True, 
            map_attrs={"center": [-71.24076894770667,-29.915835830267262], 
            "marker_color": "blue",
            "placeholder": "Elije el lugar de entrenamiento",})
    players = models.ManyToManyField(Player, through='Assistants')
    class Meta:
        verbose_name = 'Entrenamiento'
        verbose_name_plural = 'Entrenamientos'
    def __str__(self):
        return 'Entrenamiento en '+str(self.place)+', '+str(self.date)

class Assistants(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE,)
    training = models.ForeignKey(Training, on_delete=models.CASCADE,)
    observation = models.TextField()
    class Meta:
        verbose_name = 'Asistentes a entrenamineto'
        verbose_name_plural = 'Asistentes a entrenaminetos'
    def __str__(self):
        return str(self.player+" "+self.training)

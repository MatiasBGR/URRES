from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
import datetime
# Create your models here.

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):  
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    image = models.ImageField(upload_to = 'postImage/')
    def delete(self, *args, **kwargs):
        # Delete image file also
        storage, path = self.image.storage, self.image.path
        super(ImageModel, self).delete(*args, **kwargs)
        storage.delete(path)
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title



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
   measure_unit = models.CharField(max_length=100)
   info = models.TextField()
   class Meta:
       verbose_name = 'Registro'
       verbose_name_plural = 'Registros'
   def __str__(self):
        return self.name
   
    

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True,null=True)
    height = models.DecimalField(max_digits=4, decimal_places=3)
    weight = models.DecimalField(max_digits=4, decimal_places=3)
    position_one = models.ForeignKey(Position,null=True, on_delete=models.SET_NULL,)
    position_two = models.ForeignKey(Position,null=True, on_delete=models.SET_NULL,related_name='%(class)s_requests_created') 
    years_played = models.IntegerField(null=True, blank=True)
    medical_conditions =  models.TextField(blank=True)
    healthcare   = models.CharField(max_length=300)
    emergency_phone  = PhoneNumberField(null=True, blank=True)
    records = models.ManyToManyField(Record, through='Measure')
    class Meta:
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'
    def __str__(self):
        return self.user.name

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

class Directive (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True,null=True)
    position =  models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date  = models.DateField(null=True, blank=True)
    status =  models.TextField()
    class Meta:
        verbose_name = 'Directiva'
        verbose_name_plural = 'Miembros de la Directiva'
    def __str__(self):
        return str(self.position+" "+self.user.name)

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
        return str(self.opponent+" "+self.date)

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
        return str(self.player+" "+self.match)
class Training(models.Model):
    observation =  models.TextField()
    place= models.CharField(max_length=250)
    long = models.DecimalField(null=True, max_digits=9, decimal_places=6)
    lat  = models.DecimalField(null=True, max_digits=9, decimal_places=6)
    date  = models.DateField(null=True, blank=True)
    players = models.ManyToManyField(Player, through='Assistants')
    class Meta:
        verbose_name = 'Entrenamiento'
        verbose_name_plural = 'Entrenamientos'
    def __str__(self):
        return str('Entrenamiento en '+self.place+', '+self.date)

class Assistants(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE,)
    training = models.ForeignKey(Training, on_delete=models.CASCADE,)
    observation = models.TextField()
    class Meta:
        verbose_name = 'Asistentes a entrenamineto'
        verbose_name_plural = 'Asistentes a entrenaminetos'
    def __str__(self):
        return str(self.player+" "+self.training)

class Minute(models.Model):
    table = models.TextField('Tabla',)
    date = models.DateField('Fecha',)
    location =  models.CharField('Ubicación',max_length=250)
    content = models.TextField('Contenido')
    users = models.ManyToManyField(User, through='Minute_Assistants')
    class Meta:
        verbose_name = 'Acta'
        verbose_name_plural = 'Actas'
    def __str__(self):
        return str(self.table+" "+self.location)

class Minute_Assistants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    minute = models.ForeignKey(Minute, on_delete=models.CASCADE,)
    observation = models.TextField()
    class Meta:
        verbose_name = 'Asistentes a Acta'
        verbose_name_plural = 'Asistentes a Actas'
    def __str__(self):
        return str(self.user+" "+self.minute)

class Isue(models.Model):
    title =  models.CharField('Titulo',max_length=100)
    content = models.TextField('Contenido',)
    votes = models.ManyToManyField(User, through='Vote')
    minute = models.ForeignKey(Minute, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'
    def __str__(self):
        return self.title

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    isue = models.ForeignKey(Isue, on_delete=models.CASCADE, blank=True,null=True)
    on_favor = models.BooleanField(null=True)
    class Meta:
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'
        unique_together = (('user','isue'),)
    def __str__(self):
        return str(self.user.name+" voto en "+señf.isue)

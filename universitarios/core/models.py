from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from mapbox_location_field.models import LocationField
from mapbox_location_field.spatial.models import SpatialLocationField
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from vote.models import VoteModel

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

class Minute(models.Model):
    table = models.TextField('Tabla',)
    date = models.DateField('Fecha',)
    location =  models.CharField('Ubicación',max_length=250)
    locationGPS = LocationField(null=True, blank=True, 
            map_attrs={"center": [-71.24076894770667,-29.915835830267262], 
            "marker_color": "blue",
            "placeholder": "Lugar de reunión",})
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

class Isue(VoteModel,models.Model):
    title =  models.CharField('Titulo',max_length=100)
    content = models.TextField('Contenido',)
    minute = models.ForeignKey(Minute, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'
    def __str__(self):
        return self.title



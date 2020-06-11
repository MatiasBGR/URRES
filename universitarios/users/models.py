from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
# Create your models here.

def default_group(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='socio'))
post_save.connect(default_group, sender=User)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    avatar = models.ImageField(upload_to='profile_image/', null=True, blank=True)
    rut = models.CharField(max_length=30,)
    phone = PhoneNumberField('Número de telefono',)
    birth_date = models.DateField('Fecha de nacimiento', )
    incorporation_date = models.DateTimeField(default=datetime.datetime.now)
    

    def __str__(self):
        return self.user.username
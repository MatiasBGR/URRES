from django.contrib import admin

# Register your models here.
from core.models import Minute, Isue, Vote, Minute_Assistants
admin.site.register(Minute)
admin.site.register(Isue)
admin.site.register(Vote)
admin.site.register(Minute_Assistants)
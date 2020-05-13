from django.contrib import admin


# Register your models here.
from .models import Player, Position, Record, Match, Measure, Played, Training, Assistants
admin.site.register(Player)
admin.site.register(Position)
admin.site.register(Record)
admin.site.register(Match)
admin.site.register(Measure)
admin.site.register(Played)
admin.site.register(Training)
admin.site.register(Assistants)
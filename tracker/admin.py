from django.contrib import admin
from .models import Agent, Map, Player, Match, MatchEntry

# Register your models here.

admin.site.register(Agent)
admin.site.register(Map)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(MatchEntry)
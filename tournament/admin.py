from django.contrib import admin
from .models import Team, Player, Coach, Game, Rating

# Register your models here.
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Coach)
admin.site.register(Game)
admin.site.register(Rating)
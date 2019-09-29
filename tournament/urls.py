from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("scoreboard/", views.scoreboard, name="scoreboard"),
    path("players/", views.players, name="players"),
    path("game/<int:id>", views.game, name="game"),
    path("register/", views.register, name="register"),
    path("register/player/", views.regPlayer, name="regPlayer"),
    path("register/team/", views.regTeam, name="regTeam"),
    path("register/coach/", views.regCoach, name="regCoach"),
]
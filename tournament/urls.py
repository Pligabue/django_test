from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("scoreboard/", views.scoreboard, name="scoreboard"),
    path("players/", views.players, name="players"),
    path("coachsection/", views.coachSection, name="coachSection"),
    path("coachsection/login", views.loginCoach, name="loginCoach"),
    path("coachsection/logout", views.logoutCoach, name="logoutCoach"),
    path("game/<int:id>", views.game, name="game"),
    path("game/<int:id>/rating", views.addRating, name="addRating"),
    path("game/<int:id>/approve", views.approveGame, name="approveGame"),
    path("game/<int:id>/delete", views.deleteGame, name="deleteGame"),
    path("register/", views.register, name="register"),
    path("register/player/", views.regPlayer, name="regPlayer"),
    path("register/team/", views.regTeam, name="regTeam"),
    path("register/coach/", views.regCoach, name="regCoach"),
    path("register/game/", views.regGame, name="regGame"),
    path("populate/", views.populate, name="populate"),
    path("current/", views.currentUser, name="currentUser"),
]
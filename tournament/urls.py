from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("teams/", views.teams, name="teams"),
    path("signup/player/", views.signPlayer, name="signPlayer"),
]
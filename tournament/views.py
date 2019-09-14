from django.shortcuts import render
from .models import Team
from .forms import PlayerForm

# Create your views here.

def home(request):
    return render(request, "tournament/home.html")

def teams(request):
    teams = Team.objects.all()
    L = []
    for team in teams:
        team.points = 3*team.wins + 1*team.ties
        team.games = team.wins + team.losses + team.ties
        L.append(team) 
    L.sort(key=lambda x: (-x.points, -x.wins, -x.goal_difference, x.name))

    return render(request, "tournament/teams.html", {"teams" : L})

def signPlayer(request):
    form = PlayerForm()
    return render(request, "tournament/playerForm.html", {"form": form})

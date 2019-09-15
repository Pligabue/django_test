from django.shortcuts import render
from django.http import HttpResponse
from .models import Team, Player
from .forms import PlayerForm, TeamForm

# Create your views here.

def home(request):
    return render(request, "tournament/home.html")

def scoreboard(request):
    teams = Team.objects.all()
    L = []
    for team in teams:
        team.points = 3*team.wins + 1*team.ties
        team.games = team.wins + team.losses + team.ties
        L.append(team) 
    L.sort(key=lambda x: (-x.points, -x.wins, -x.goal_difference, x.name))

    return render(request, "tournament/scoreboard.html", {"teams" : L})

def players(request):
    players = Player.objects.all()
    return render(request, "tournament/players.html", {"players" : players})

def regPlayer(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            player = Player(team=data["team"], name=data["name"], surname=data["surname"], birthday=data["birthday"])
            player.save()
            return HttpResponse("Foi")
        return render(request, "tournament/playerForm.html", {"form": form})
    else:
        form = PlayerForm()
        return render(request, "tournament/playerForm.html", {"form": form})


def regTeam(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            player = Team(name=data["name"], founded=data["founded"])
            player.save()
            return HttpResponse("Foi")
        return render(request, "tournament/teamForm.html", {"form": form})
    else:
        form = TeamForm()
        return render(request, "tournament/teamForm.html", {"form": form})







from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max
from .models import Team, Player, Game, Rating
from .forms import PlayerForm, TeamForm

# Create your views here.

def home(request):
    return render(request, "tournament/home.html")

def scoreboard(request):
    teams = Team.objects.all()
    teamList = []

    for team in teams:
        team.wins = 0
        team.ties = 0
        team.losses = 0
        team.goal_difference = 0

        homeGames = Game.objects.filter(team_1=team)
        for game in homeGames:
            if game.score_team_1 != None and game.score_team_2 != None:
                if game.score_team_1 > game.score_team_2:
                    team.wins += 1
                elif game.score_team_1 == game.score_team_2:
                    team.ties += 1
                else:
                    team.losses += 1
                team.goal_difference += game.score_team_1 - game.score_team_2

        awayGames = Game.objects.filter(team_2=team)
        for game in awayGames:
            if game.score_team_1 != None and game.score_team_2 != None:
                if game.score_team_1 < game.score_team_2:
                    team.wins += 1
                elif game.score_team_1 == game.score_team_2:
                    team.ties += 1
                else:
                    team.losses += 1
                team.goal_difference += game.score_team_2 - game.score_team_1
            
        team.points = 3*team.wins + 1*team.ties
        team.games = team.wins + team.losses + team.ties
        teamList.append(team) 
    teamList.sort(key=lambda x: (-x.points, -x.wins, -x.goal_difference, x.name))
    
    games = Game.objects.all()
    try:
        rounds = games.aggregate(Max("round"))["round__max"]
        rounds = reversed(range(1, rounds+1))
    except:
        rounds = []

    return render(request, "tournament/scoreboard.html", {"teams" : teamList, "games": games, "rounds": rounds})

def players(request):
    players = Player.objects.all()
    for player in players:
        player.nGames = len(player.games.all())
        ratings = player.ratings.all()
        if ratings:
            player.rating = 0.0
            for i, rating in enumerate(ratings):
                player.rating += float(rating.rating)
            player.rating = player.rating/(i+1)
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

def game(request, id):
    game = Game.objects.get(pk=id)
    ratings = Rating.objects.filter(game=game)
    home_players = []
    away_players = []
    for rating in ratings:
        if rating.player.team == game.team_1:
            home_players.append(rating.player)
        elif rating.player.team == game.team_2:
            away_players.append(rating.player)
    return render(request, "tournament/game.html", {"game": game, "home_players": home_players, "away_players": away_players})




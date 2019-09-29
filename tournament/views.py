from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max
from django.contrib.auth.models import User
from .models import Team, Player, Game, Rating, Coach
from .forms import PlayerForm, TeamForm, CoachForm

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

def game(request, id):
    game = Game.objects.get(pk=id)
    ratings = Rating.objects.filter(game=game)
    home_ratings = []
    away_ratings = []
    for rating in ratings:
        if rating.player.team == game.team_1:
            home_ratings.append(rating)
        elif rating.player.team == game.team_2:
            away_ratings.append(rating)
    return render(request, "tournament/game.html", {"game": game, "home_ratings": home_ratings, "away_ratings": away_ratings})

def register(request):
    return render(request, "tournament/register.html")

def regPlayer(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            player = Player(team=data["team"], name=data["name"], surname=data["surname"], birthday=data["birthday"])
            player.save()
            return render(request, "tournament/success.html", {"name": "player"})
        return render(request, "tournament/playerForm.html", {"form": form})
    else:
        form = PlayerForm()
        return render(request, "tournament/playerForm.html", {"form": form})


def regTeam(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            team = Team(name=data["name"], founded=data["founded"])
            team.save()
            return render(request, "tournament/success.html", {"name": "team"})
        return render(request, "tournament/teamForm.html", {"form": form})
    else:
        form = TeamForm()
        return render(request, "tournament/teamForm.html", {"form": form})

def regCoach(request):
    if request.method == "POST":
        form = CoachForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user = User(username=(data["name"]+data["surname"]), password=data["password"], first_name=data["name"], last_name=data["surname"])
            try:
                user.save()
            except Exception as error:
                print(error)
                return render(request, "tournament/coachForm.html", {"form": form})
            coach = Coach(user=user, team=data["team"], birthday=data["birthday"])
            try:    
                coach.save()
            except Exception as error:
                print(error)
                user.delete()
                return render(request, "tournament/coachForm.html", {"form": form})
            return render(request, "tournament/success.html", {"name": "coach"})
        return render(request, "tournament/coachForm.html", {"form": form})
    else:
        form = CoachForm()
        return render(request, "tournament/coachForm.html", {"form": form})


def populate(request):

    team1 = Team(name="Timaço", founded="1981-09-12")
    team1.save()
    team2 = Team(name="Time Antigo", founded="1019-02-05")
    team2.save()
    team3 = Team(name="Timinho", founded="1019-02-05")
    team3.save()
    team4 = Team(name="Pior Time da História", founded="2019-09-17")
    team4.save()

    player1 = Player(team=team1, name="Cerginho", surname="da Pereira Nunes", birthday="1977-10-26")
    player1.save()
    player2 = Player(team=team3, name="Craque", surname="Daniel", birthday="1980-04-07")
    player2.save()
    player3 = Player(team=team4, name="Pior jogador da história", surname="(é sério)", birthday="2000-09-17")
    player3.save()
    player4 = Player(team=team3, name="Julinho", surname="da Van", birthday="1981-05-25")
    player4.save()
    player5 = Player(team=team2, name="Seu Getúlio", surname="do Grunge", birthday="1900-02-22")
    player5.save()
    player6 = Player(team=team1, name="Poeta", surname="de Sunga", birthday="1985-10-10")
    player6.save()



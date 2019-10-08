from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Max, Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, password_validation, login, logout
from django.urls import reverse
from .models import Team, Player, Game, Rating, Coach
from .forms import PlayerForm, TeamForm, CoachForm, LoginForm, RatingForm, GameForm

# Create your views here.

def coach_required(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        current_user = request.user
        if current_user.is_authenticated:
            if hasattr(current_user, "coach"):
                response = func(*args, **kwargs)
                return response
            else:
                return redirect(logoutCoach)
        else:
            return redirect(loginCoach)
    return wrapper

def home(request):
    return render(request, "tournament/home.html")

def scoreboard(request):
    teams = Team.objects.all()

    for team in teams:
        team.wins = 0
        team.ties = 0
        team.losses = 0
        team.goal_difference = 0

        homeGames = Game.objects.filter(team_1=team, approved_1=True, approved_2=True)
        for game in homeGames:
            if game.score_team_1 != None and game.score_team_2 != None:
                if game.score_team_1 > game.score_team_2:
                    team.wins += 1
                elif game.score_team_1 == game.score_team_2:
                    team.ties += 1
                else:
                    team.losses += 1
                team.goal_difference += game.score_team_1 - game.score_team_2

        awayGames = Game.objects.filter(team_2=team, approved_1=True, approved_2=True)
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
    teams = sorted(teams, key=lambda x: (-x.points, -x.wins, -x.goal_difference, x.name))
    
    games = Game.objects.filter(approved_1=True, approved_2=True)
    try:
        rounds = games.aggregate(Max("round"))["round__max"]
        rounds = reversed(range(1, rounds+1))
    except:
        rounds = []

    return render(request, "tournament/scoreboard.html", {"teams" : teams, "games": games, "rounds": rounds})

def players(request):
    players = Player.objects.all()
    for player in players:
        player.nGames = len(player.games.all())
        ratings = player.ratings.all()
        if ratings:
            player.rating = 0.0
            for i, rating in enumerate(ratings):
                player.rating += float(rating.rating)
            player.rating = round(player.rating/(i+1), 2)
    players = sorted(players, key=lambda x: (-x.nGames, x.name))
    return render(request, "tournament/players.html", {"players" : players})

def loginCoach(request):
 
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            username = data["full_name"].replace(" ", "_")
            user = authenticate(username=username, password=data["password"])

            if user is not None:
                login(request, user)
                return redirect(coachSection)
            else:
                messages.error(request, "*Invalid username or password")
                return render(request, "tournament/form.html", {"form": form, "title": "Log In", "url": "/tournament/coachsection/login"})
    else:
        form = LoginForm()
        return render(request, "tournament/form.html", {"form": form, "title": "Log In", "url": "/tournament/coachsection/login"})

def logoutCoach(request):
    logout(request)
    return redirect(loginCoach)

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

    team_1_coach, team_2_coach = False, False
    current_user = request.user
    if current_user.is_authenticated:
        if hasattr(current_user, "coach"):
            if current_user.coach.team == game.team_1:
                team_1_coach = True
            elif current_user.coach.team == game.team_2:
                team_2_coach = True

    return render(request, "tournament/game.html", {"game": game, "home_ratings": home_ratings, "away_ratings": away_ratings, "team_1_coach": team_1_coach, "team_2_coach": team_2_coach, })

@coach_required
def coachSection(request):
    current_user = request.user
    team = current_user.coach.team
    players = Player.objects.filter(team=current_user.coach.team)
    for player in players:
        ratings = player.ratings.all()
        if len(ratings) == 0:
            continue
        player.rating = 0.0
        for rating in ratings:
            player.rating += float(rating.rating)
        player.rating = round(player.rating/len(ratings), 2)
    games = Game.objects.filter(Q(approved_1=True, approved_2=True) & (Q(team_1=team) | Q(team_2=team))).order_by("-round")
    notApproved = Game.objects.filter(Q(team_1=team, approved_1=False) | Q(team_2=team, approved_2=False))
    pending = Game.objects.filter(Q(team_1=team, approved_2=False) | Q(team_2=team, approved_1=False))
    return render(request, "tournament/coachSection.html", {
        "user": current_user,
        "players": players,
        "numPlayers": len(players),
        "games": games, 
        "numGames": len(games),
        "notApproved": notApproved,
        "pending": pending,
    })

@coach_required
def addRating(request, id):

    current_user = request.user
    team = current_user.coach.team
    game = Game.objects.get(pk=id)

    if request.method == "POST":
        form = RatingForm(team, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            rating = Rating.objects.filter(game=game, player=data["player"]).first()
            if rating is None:
                rating = Rating(game=game, player=data["player"], rating=data["rating"])
                rating.save()
            else:
                rating.rating = data["rating"] 
                rating.save()
            return redirect(coachSection)
        else:
            form = RatingForm(team)
            return render(request, "tournament/form.html", {"form": form, "title": "Rate Player", "url": ("/tournament/game/" + str(id) + "/rating")})
    else:
        form = RatingForm(team)
        return render(request, "tournament/form.html", {"form": form, "title": "Rate Player", "url": ("/tournament/game/" + str(id) + "/rating")})

@coach_required
def approveGame(request, id):
    current_user = request.user
    team = current_user.coach.team
    game = Game.objects.get(pk=id)
    if game.team_1 == team and game.approved_1 == False:
        game.approved_1 = True
        game.save()
    elif game.team_2 == team and game.approved_2 == False:
        game.approved_2 = True
        game.save()
    return redirect(coachSection)

@coach_required
def deleteGame(request, id):
    current_user = request.user
    team = current_user.coach.team
    game = Game.objects.get(pk=id)
    if game.team_1 == team and game.approved_1 == False:
        game.delete()
    elif game.team_2 == team and game.approved_2 == False:
        game.delete()
    return redirect(coachSection)

def register(request):
    isCoach = False
    current_user = request.user
    if current_user.is_authenticated:
        if hasattr(current_user, "coach"):
            isCoach = True
    return render(request, "tournament/register.html", {"isCoach": isCoach})

def regTeam(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            team = Team(name=data["name"], founded=data["founded"])
            team.save()
            return render(request, "tournament/success.html", {"name": "team"})
        return render(request, "tournament/form.html", {"form": form, "title": "Register Team", "url": "/tournament/register/team/"})
    else:
        form = TeamForm()
        return render(request, "tournament/form.html", {"form": form, "title": "Register Team", "url": "/tournament/register/team/"})

@coach_required
def regPlayer(request):
    current_user = request.user
    team = current_user.coach.team
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            player = Player(team=team, name=data["name"], surname=data["surname"], birthday=data["birthday"])
            player.save()
            return render(request, "tournament/success.html", {"name": "player"})
        return render(request, "tournament/form.html", {"form": form, "title": "Register Player", "url": "/tournament/register/player/"})
    else:
        form = PlayerForm()
        return render(request, "tournament/form.html", {"form": form, "title": "Register Player - " + str(team), "url": "/tournament/register/player/"})

def regCoach(request):
    if request.method == "POST":
        form = CoachForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                username = (data["first_name"]+"_"+data["last_name"]).replace(" ", "_")
                user = User(username=username, first_name=data["first_name"], last_name=data["last_name"])
                user.set_password(data["password1"])
                user.save()
            except Exception as error:
                print("ERROR:", error)
                return render(request, "tournament/form.html", {"form": form, "title": "Register Coach", "url": "/tournament/register/coach/"})
            try:    
                coach = Coach(user=user, team=data["team"], birthday=data["birthday"])
                coach.save()
            except Exception as error:
                print("ERROR:", error)
                user.delete()
                return render(request, "tournament/form.html", {"form": form, "title": "Register Coach", "url": "/tournament/register/coach/"})
            return render(request, "tournament/success.html", {"name": "coach"})
        return render(request, "tournament/form.html", {"form": form, "title": "Register Coach", "url": "/tournament/register/coach/"})
    else:
        form = CoachForm()
        return render(request, "tournament/form.html", {"form": form, "title": "Register Coach", "url": "/tournament/register/coach/"})

@coach_required
def regGame(request):
    current_user = request.user
    team = current_user.coach.team

    if request.method == "POST":
        form = GameForm(team, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            round = data["round"]
            if data["home"]:
                team_1 = team
                team_2 = data["opponent"]
                score_team_1 = data["my_score"]
                score_team_2 = data["opponent_score"]
                approved_1 = True
                approved_2 = False
            else:
                team_1 = data["opponent"]
                team_2 = team
                score_team_1 = data["opponent_score"]
                score_team_2 = data["my_score"]
                approved_1 = False
                approved_2 = True
            game = Game.objects.filter(Q(round=round), Q(team_1=team_1) | Q(team_2=team_1) | Q(team_1=team_2) | Q(team_2=team_2)).first()
            if game is None:
                game = Game(round=round, team_1=team_1, team_2=team_2, score_team_1=score_team_1, score_team_2=score_team_2, approved_1=approved_1, approved_2=approved_2)
                game.save()
                return redirect(coachSection)
            else:
                messages.error(request, "*At least one of the teams already has a game in this round.")
                return render(request, "tournament/form.html", {"form": form, "title": "New Game", "url": "/tournament/register/game/"})
    else:
        form = GameForm(team)
        return render(request, "tournament/gameForm.html", {"form": form, "url": "/tournament/register/game/"})


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

def currentUser(request):
    current_user = request.user
    if current_user.is_authenticated:
        return HttpResponse(str(current_user.coach) + ", " + str(current_user.coach.team) + "'s coach")
    else:
        return HttpResponse("No user") 

from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    founded = models.DateField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    ties = models.IntegerField()
    goal_difference = models.IntegerField()

    def __str__(self):
        return self.name


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birthday = models.DateField()
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    games = models.IntegerField()

    def __str__(self):
        return self.name
    

class Coach(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
        return self.name


class Game(models.Model):
    team_1 = models.ForeignKey(Team,on_delete=models.CASCADE, related_name="+")
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="+")
    score_team_1 = models.IntegerField()
    score_team_2 = models.IntegerField()

    def __str__(self):
        return (str(self.team_1) + " v " + str(self.team_2) + "(" + str(self.score_team_1) + " x " + str(self.score_team_2) + ")")


class GamePlayerMap(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=4, decimal_places=2, default=5.00)
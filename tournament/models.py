from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    founded = models.DateField()
    games_played = models.IntegerField()
    points = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    ties = models.IntegerField()
    goal_diff = models.IntegerField()

    def __str__(self):
        return self.name


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    bday = models.DateField()
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    games = models.IntegerField()

    def __str__(self):
        return self.name
    

class Coach(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    bday = models.DateField()

    def __str__(self):
        return self.name
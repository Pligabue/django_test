from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    founded = models.DateField()

    def __str__(self):
        return self.name

class Game(models.Model):
    round = models.IntegerField(default=1)
    team_1 = models.ForeignKey(Team,on_delete=models.CASCADE, related_name="home")
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away")
    score_team_1 = models.IntegerField(null=True, blank=True)
    score_team_2 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return (str(self.round) + ": " + str(self.team_1) + " vs " + str(self.team_2) + " (" + str(self.score_team_1) + " x " + str(self.score_team_2) + ")")

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birthday = models.DateField()
    games = models.ManyToManyField(Game, through="Rating")

    def __str__(self):
        return self.name
    
class Rating(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="ratings")
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.game) + " : " + str(self.player)


class Coach(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
        return self.name



from django import forms
from django.db.models import Max, Q
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Team, Coach, Player, Game

from datetime import datetime

class PlayerForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    surname = forms.CharField(label="Surname", max_length=100)
    birthday = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'founded']
        widgets = {
            "founded": forms.DateInput(attrs={"type": "date"})
        }

class CoachForm(UserCreationForm):
    team = forms.ModelChoiceField(queryset=Team.objects.filter(coach=None))
    birthday = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    
    class Meta:
        model = User
        fields = ("team", 'first_name', 'last_name', "birthday", 'password1', 'password2', )
        help_texts = {
            'password1': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None
    
class GameForm(forms.Form):
    round = forms.IntegerField(min_value=1, max_value=(Game.objects.all().aggregate(Max("round"))["round__max"] + 1), initial=(Game.objects.all().aggregate(Max("round"))["round__max"] + 1))
    home = forms.BooleanField(required=False)
    opponent = forms.ModelChoiceField(queryset=Team.objects.none())
    my_score = forms.IntegerField(min_value=0, initial=0, label="Your team's score")
    opponent_score = forms.IntegerField(min_value=0, initial=0, label="Opponent's score")
    
    def __init__(self, team, *args, **kwargs):     
        super().__init__(*args, **kwargs)
        self.fields["opponent"].queryset = Team.objects.exclude(id=team.id)

    
class LoginForm(forms.Form):
    full_name = forms.CharField(label="Full Name")
    password = forms.CharField(widget=forms.PasswordInput())


class RatingForm(forms.Form):
    player = forms.ModelChoiceField(queryset=Player.objects.none()) 
    rating = forms.DecimalField(max_value=10.00, min_value=0.00, max_digits=4, initial=5.00)
    
    def __init__(self, team, *args, **kwargs):     
        super().__init__(*args, **kwargs)
        self.fields["player"].queryset = Player.objects.filter(team=team)
        
        


        
        
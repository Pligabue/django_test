from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Team, Coach

from datetime import datetime

class PlayerForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all())
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
    
    
    
class LoginForm(forms.Form):
    full_name = forms.CharField(label="Full Name")
    password = forms.CharField(widget=forms.PasswordInput())
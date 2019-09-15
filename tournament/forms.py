from django import forms
from .models import Team

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
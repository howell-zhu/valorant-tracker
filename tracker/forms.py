from django import forms
from django.forms import inlineformset_factory
from .models import Match, MatchEntry, Player, Agent, Map, RANK_CHOICES

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['date', 'map', 'team_a_score', 'team_b_score', 'duration_minutes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class MatchEntryForm(forms.ModelForm):
    class Meta:
        model = MatchEntry
        fields = ['player', 'agent', 'team', 'rank_at_match', 'kills', 'deaths', 'assists']

class MatchFilterForm(forms.Form):
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    map = forms.ModelChoiceField(
        queryset=Map.objects.all(),
        required=False,
        empty_label='All Maps'
    )

MatchEntryFormSet = inlineformset_factory(
    Match,
    MatchEntry, 
    form=MatchEntryForm,
    extra=10, 
    can_delete=True
)

MatchEntryEditFormSet = inlineformset_factory(
    Match,
    MatchEntry,
    form=MatchEntryForm,
    extra=0,
    can_delete=True
)
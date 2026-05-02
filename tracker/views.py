from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction, connection
from .models import Match, MatchEntry, RANK_ORDER
from .forms import MatchForm, MatchEntryFormSet, MatchEntryEditFormSet, MatchFilterForm

def add_match(request):
    if request.method == 'POST':
        match_form = MatchForm(request.POST)
        entry_formset = MatchEntryFormSet(request.POST)

        if match_form.is_valid() and entry_formset.is_valid():
            match = match_form.save(commit=False)

            entries_data = entry_formset.cleaned_data
            ranks = [
                RANK_ORDER[e['rank_at_match']]
                for e in entries_data
                if e and not e.get('DELETE') and e.get('rank_at_match')
            ]
            if ranks:
                avg_value = round(sum(ranks) / len(ranks))
                avg_value = max(1, min(avg_value, 25)) 
                match.avg_lobby_rank = next(
                    r for r, v in RANK_ORDER.items() if v == avg_value
                )

            match.save()

            entry_formset.instance = match
            entry_formset.save()

            return redirect('match_list')

    else:
        match_form = MatchForm()
        entry_formset = MatchEntryFormSet()

    return render(request, 'tracker/add_match.html', {
        'match_form': match_form,
        'entry_formset': entry_formset,
    })

@transaction.atomic
def edit_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if request.method == 'POST':
        match_form = MatchForm(request.POST, instance=match)
        entry_formset = MatchEntryEditFormSet(request.POST, instance=match)

        if match_form.is_valid() and entry_formset.is_valid():
            match = match_form.save(commit=False)

            entries_data = entry_formset.cleaned_data
            ranks = [
                RANK_ORDER[e['rank_at_match']]
                for e in entries_data
                if e and not e.get('DELETE') and e.get('rank_at_match')
            ]
            if ranks:
                avg_value = round(sum(ranks) / len(ranks))
                avg_value = max(1, min(avg_value, 25))
                match.avg_lobby_rank = next(
                    r for r, v in RANK_ORDER.items() if v == avg_value
                )

            match.save()
            entry_formset.save()

            return redirect('match_list')

    else:
        match_form = MatchForm(instance=match)
        entry_formset = MatchEntryEditFormSet(instance=match)

    return render(request, 'tracker/edit_match.html', {
        'match_form': match_form,
        'entry_formset': entry_formset,
        'match': match,
    })

def delete_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if request.method == 'POST':
        match.delete()
        return redirect('match_list')

    return render(request, 'tracker/delete_match.html', {
        'match': match,
    })

def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    entries = MatchEntry.objects.filter(match=match)

    team_a_entries = entries.filter(team='A')
    team_b_entries = entries.filter(team='B')

    return render(request, 'tracker/match_detail.html', {
        'match': match,
        'team_a_entries': team_a_entries,
        'team_b_entries': team_b_entries,
    })

def match_list(request):
    filter_form = MatchFilterForm(request.GET)
    date = None
    map_id = None

    if filter_form.is_valid():
        date = filter_form.cleaned_data.get('date')
        selected_map = filter_form.cleaned_data.get('map')
        if selected_map:
            map_id = selected_map.id

    if date and map_id:
        matches = Match.objects.raw('''
            SELECT m.id, m.date, map.name AS map_name, m.team_a_score,
                   m.team_b_score, m.duration_minutes, m.avg_lobby_rank
            FROM tracker_match m
            JOIN tracker_map map ON m.map_id = map.id
            WHERE m.date = %s AND m.map_id = %s
            ORDER BY m.date DESC
        ''', [date, map_id])
    elif date:
        matches = Match.objects.raw('''
            SELECT m.id, m.date, map.name AS map_name, m.team_a_score,
                   m.team_b_score, m.duration_minutes, m.avg_lobby_rank
            FROM tracker_match m
            JOIN tracker_map map ON m.map_id = map.id
            WHERE m.date = %s
            ORDER BY m.date DESC
        ''', [date])
    elif map_id:
        matches = Match.objects.raw('''
            SELECT m.id, m.date, map.name AS map_name, m.team_a_score,
                   m.team_b_score, m.duration_minutes, m.avg_lobby_rank
            FROM tracker_match m
            JOIN tracker_map map ON m.map_id = map.id
            WHERE m.map_id = %s
            ORDER BY m.date DESC
        ''', [map_id])
    else:
        matches = Match.objects.raw('''
            SELECT m.id, m.date, map.name AS map_name, m.team_a_score,
                   m.team_b_score, m.duration_minutes, m.avg_lobby_rank
            FROM tracker_match m
            JOIN tracker_map map ON m.map_id = map.id
            ORDER BY m.date DESC
        ''')

    return render(request, 'tracker/match_list.html', {
        'matches': matches,
        'filter_form': filter_form,
    })
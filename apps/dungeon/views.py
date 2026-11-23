from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery
from django.utils import timezone
from django.contrib import messages
from apps.profiles.models import Profile
from django.views.decorators.http import require_POST

# Ensure ALL models used in this file are imported here
from .models import Deck, Card, StudySession, CardReview
from .forms import DeckForm, CardForm

@login_required
def forge_dungeon_view(request):
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.user = request.user
            deck.save()
            messages.success(request, f'"{deck.name}" has been forged!')
            return redirect('dungeon:dungeon_detail', deck_id=deck.pk)
    else:
        form = DeckForm()

    return render(request, 'dungeon/forge_dungeon.html', {'form': form})


@login_required
def dungeon_detail_view(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id, user=request.user)

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.save()
            messages.success(request, 'A new enemy has spawned in the dungeon!')
            return redirect('dungeon:dungeon_detail', deck_id=deck.pk)
    else:
        form = CardForm()

    cards = Card.objects.filter(deck=deck).order_by('-created_at')
    return render(request, 'dungeon/dungeon_detail.html', {
        'deck': deck,
        'cards': cards,
        'form': form,
    })


# ---------------------------------------------------------------------------
# Edit / delete: decks and cards (always scoped to the logged-in user)
# ---------------------------------------------------------------------------
@login_required
def edit_deck_view(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id, user=request.user)

    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{deck.name}" has been reforged!')
            return redirect('dungeon:dungeon_detail', deck_id=deck.pk)
    else:
        form = DeckForm(instance=deck)

    return render(request, 'dungeon/edit_deck.html', {'form': form, 'deck': deck})


@login_required
@require_POST
def delete_deck_view(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id, user=request.user)
    name = deck.name
    deck.delete()  # cascades to cards, runs and reviews
    messages.success(request, f'"{name}" has been collapsed and sealed forever.')
    return redirect('home:home')


@login_required
def edit_card_view(request, card_id):
    card = get_object_or_404(Card, pk=card_id, deck__user=request.user)

    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'The enemy has been reshaped.')
            return redirect('dungeon:dungeon_detail', deck_id=card.deck_id)
    else:
        form = CardForm(instance=card)

    return render(request, 'dungeon/edit_card.html', {'form': form, 'card': card})


@login_required
@require_POST
def delete_card_view(request, card_id):
    card = get_object_or_404(Card, pk=card_id, deck__user=request.user)
    deck_id = card.deck_id
    card.delete()
    messages.success(request, 'The enemy has been banished.')
    return redirect('dungeon:dungeon_detail', deck_id=deck_id)


MONSTERS = [
    ("spider", "A Giant Cave Spider drops from the ceiling!"),
    ("skull", "A Restless Skull rattles out of the dark!"),
    ("bat", "A Cave Bat swoops down at you!"),
]


@login_required
@require_POST
def start_run_view(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id, user=request.user)

    if not Card.objects.filter(deck=deck).exists():
        messages.error(request, "This dungeon is empty! Spawn enemies first.")
        return redirect('dungeon:dungeon_detail', deck_id=deck.pk)

    session = StudySession.objects.create(user=request.user, deck=deck)
    return redirect('dungeon:review_run', session_id=session.pk)


@login_required
def review_run_view(request, session_id):
    session = get_object_or_404(StudySession, pk=session_id, user=request.user)

    # Already finished: go straight to the loot screen
    if session.ended_at:
        return redirect('dungeon:run_results', session_id=session.pk)

    reviewed_card_ids = CardReview.objects.filter(session=session).values_list('card_id', flat=True)
    next_card = Card.objects.filter(deck=session.deck).exclude(id__in=reviewed_card_ids).first()

    # No cards left: finish the run and award XP
    if not next_card:
        session.ended_at = timezone.now()
        session.xp_earned = session.enemies_killed * 15
        session.save()

        profile, _ = Profile.objects.get_or_create(user=request.user)
        old_level = profile.level
        profile.total_cards_memorized += session.enemies_killed
        profile.add_xp(session.xp_earned)  # add_xp saves the profile itself

        if profile.level > old_level:
            messages.success(request, f"Rank up! You have reached Rank {profile.level}.")

        return redirect('dungeon:run_results', session_id=session.pk)

    # Combat action
    if request.method == 'POST':
        action = request.POST.get('action')  # 'kill' or 'run'
        if action in ('kill', 'run'):
            is_successful = (action == 'kill')
            CardReview.objects.create(session=session, card=next_card, is_successful=is_successful)
            if is_successful:
                session.enemies_killed += 1
            else:
                session.times_ran_away += 1
            session.save()
        return redirect('dungeon:review_run', session_id=session.pk)

    monster_kind, monster_caption = MONSTERS[next_card.pk % len(MONSTERS)]
    total = Card.objects.filter(deck=session.deck).count()
    done = session.enemies_killed + session.times_ran_away
    return render(request, 'dungeon/review_card.html', {
        'session': session,
        'card': next_card,
        'monster_kind': monster_kind,
        'monster_caption': monster_caption,
        'room_number': done + 1,
        'total': total,
        'progress_percent': min(100, int(done / total * 100)) if total else 0,
    })


@login_required
def run_results_view(request, session_id):
    session = get_object_or_404(StudySession, pk=session_id, user=request.user)

    total = session.enemies_killed + session.times_ran_away
    accuracy = int(session.enemies_killed / total * 100) if total else 0
    if accuracy == 100:
        rank = "S"
    elif accuracy >= 75:
        rank = "A"
    elif accuracy >= 50:
        rank = "B"
    else:
        rank = "C"

    profile, _ = Profile.objects.get_or_create(user=request.user)
    xp_needed = profile.get_xp_for_next_level()

    return render(request, 'dungeon/run_results.html', {
        'session': session,
        'accuracy': accuracy,
        'rank': rank,
        'profile': profile,
        'xp_needed': xp_needed,
        'progress_percent': int(profile.current_xp / xp_needed * 100) if xp_needed else 0,
    })


# ---------------------------------------------------------------------------
# ACTIVITY 1: SQL JOIN
# StudySession (many) --> Deck (one), joined on study_session.deck_id = deck.id
# ---------------------------------------------------------------------------
@login_required
def run_history_view(request):
    sessions = (
        StudySession.objects
        .filter(user=request.user, ended_at__isnull=False)
        .select_related('deck')          # <-- the JOIN
        .order_by('-ended_at')
    )
    return render(request, 'dungeon/run_history.html', {
        'sessions': sessions,
        'sql': str(sessions.query) if settings.DEBUG else None,
    })


# ---------------------------------------------------------------------------
# ACTIVITY 2: SQL SUBQUERY
# Outer query: cards. Inner query: card ids the user has fled at least once.
# ---------------------------------------------------------------------------
@login_required
def cursed_foes_view(request):
    fled_card_ids = (
        CardReview.objects
        .filter(session__user=request.user, is_successful=False)
        .values('card_id')               # inner query
    )
    cards = (
        Card.objects
        .filter(id__in=Subquery(fled_card_ids))   # outer query uses the inner one
        .order_by('-updated_at')
    )
    return render(request, 'dungeon/cursed_foes.html', {
        'cards': cards,
        'sql': str(cards.query) if settings.DEBUG else None,
    })
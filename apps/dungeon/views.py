from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

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
            return redirect('dungeon:dungeon_detail', deck_id=deck.pk)
    else:
        form = DeckForm()
        
    return render(request, 'dungeon/forge_dungeon.html')

@login_required
def dungeon_detail_view(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id, user=request.user)
    
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.save()
            return redirect('dungeon:dungeon_detail', deck_id=deck.pk)
            
    return render(request, 'dungeon/dungeon_detail.html', {'deck': deck})

@login_required
def start_run_view(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id, user=request.user)
    
    # Querying the Card model directly satisfies Pylance
    if Card.objects.filter(deck=deck).count() == 0:
        messages.error(request, "This dungeon is empty! Spawn enemies first.")
        return redirect('dungeon:dungeon_detail', deck_id=deck.pk)
        
    # Instantiate the adventure run
    session = StudySession.objects.create(user=request.user, deck=deck)
    return redirect('dungeon:review_run', session_id=session.pk)

@login_required
def review_run_view(request, session_id):
    session = get_object_or_404(StudySession, pk=session_id, user=request.user)
    
    # Querying CardReview directly avoids Pylance errors on session.reviews
    reviewed_card_ids = CardReview.objects.filter(session=session).values_list('card_id', flat=True)
    
    # Querying Card directly avoids Pylance errors on session.deck.cards
    next_card = Card.objects.filter(deck=session.deck).exclude(id__in=reviewed_card_ids).first()
    
    # If no cards are left, the dungeon is clear
    if not next_card:
        if not session.ended_at:
            session.ended_at = timezone.now()
            
            # Calculate XP (e.g., 15 XP per successful recall)
            xp_gained = session.enemies_killed * 15
            session.xp_earned = xp_gained
            session.save()
            
            # Apply XP and stats to the user's Profile
            profile = request.user.profile
            profile.total_cards_memorized += session.enemies_killed
            profile.add_xp(xp_gained)
            profile.save()
            
        return redirect('dungeon:run_results', session_id=session.pk)

    if request.method == 'POST':
        action = request.POST.get('action') # Expected values: 'kill' or 'run'
        is_successful = (action == 'kill')
        
        # Record the individual strike
        CardReview.objects.create(
            session=session,
            card=next_card,
            is_successful=is_successful
        )
        
        if is_successful:
            session.enemies_killed += 1
        else:
            session.times_ran_away += 1
            
        session.save()
        return redirect('dungeon:review_run', session_id=session.pk)

    return render(request, 'dungeon/review_card.html', {'session': session, 'card': next_card})

@login_required
def run_results_view(request, session_id):
    session = get_object_or_404(StudySession, pk=session_id, user=request.user)
    return render(request, 'dungeon/run_results.html', {'session': session})
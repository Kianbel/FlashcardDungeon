from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Deck, Card
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
    # Ensures a user can only access their own dungeons
    deck = get_object_or_404(Deck, pk=deck_id, user=request.user)
    
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.save()
            return redirect('dungeon:dungeon_detail', deck_id=deck.pk)
            
    return render(request, 'dungeon/dungeon_detail.html', {'deck': deck})
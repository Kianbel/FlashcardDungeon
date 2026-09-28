from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home_view(request):
    # Retrieve all decks owned by the logged-in user
    decks = request.user.decks.all().order_by('-updated_at')
    return render(request, "home/home.html", {"decks": decks})
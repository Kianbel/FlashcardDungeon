from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from apps.profiles.models import Profile


@login_required
def home_view(request):
    decks = request.user.decks.annotate(card_total=Count("cards")).order_by("-updated_at")

    # get_or_create so users created outside the register page (e.g. admin) don't crash
    profile, _ = Profile.objects.get_or_create(user=request.user)
    xp_needed = profile.get_xp_for_next_level()
    progress_percent = int(profile.current_xp / xp_needed * 100) if xp_needed else 0

    return render(request, "home/home.html", {
        "decks": decks,
        "profile": profile,
        "xp_needed": xp_needed,
        "progress_percent": progress_percent,
    })
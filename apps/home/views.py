from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render

from apps.profiles.models import Profile


@login_required
def home_view(request):
    decks = (
        request.user.decks
        .annotate(
            card_total=Count("cards", distinct=True),
            runs_done=Count("sessions", filter=Q(sessions__ended_at__isnull=False), distinct=True),
        )
        .order_by("-updated_at")
    )

    # get_or_create so users created outside the register page (e.g. admin) don't crash
    profile, _ = Profile.objects.get_or_create(user=request.user)
    xp_needed = profile.get_xp_for_next_level()
    progress_percent = int(profile.current_xp / xp_needed * 100) if xp_needed else 0
    runs_completed = request.user.study_sessions.filter(ended_at__isnull=False).count()

    return render(request, "home/home.html", {
        "decks": decks,
        "profile": profile,
        "xp_needed": xp_needed,
        "progress_percent": progress_percent,
        "runs_completed": runs_completed,
    })
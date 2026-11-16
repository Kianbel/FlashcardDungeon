from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Profile, Title


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    xp_needed = profile.get_xp_for_next_level()
    progress_percent = int(profile.current_xp / xp_needed * 100) if xp_needed else 0

    return render(request, 'profiles/profiles.html', {
        'profile': profile,
        'xp_needed': xp_needed,
        'progress_percent': progress_percent,
        'unlocked_titles': profile.unlocked_titles.all(),
        'runs_completed': request.user.study_sessions.filter(ended_at__isnull=False).count(),
    })


@login_required
def equip_title_view(request):
    if request.method == 'POST':
        profile, _ = Profile.objects.get_or_create(user=request.user)
        title_id = request.POST.get('title_id')
        if title_id:
            try:
                # Only titles the user actually owns can be equipped
                title = profile.unlocked_titles.get(id=title_id)
                profile.equipped_title = title
                profile.save()
                messages.success(request, f'You are now known as "{title.name}".')
            except (Title.DoesNotExist, ValueError):
                messages.error(request, 'You do not own that title.')
    return redirect('profiles:profiles')
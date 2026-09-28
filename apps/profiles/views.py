from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Title

@login_required
def profile_view(request):
    profile = request.user.profile
    xp_needed = profile.get_xp_for_next_level()
    
    # Calculate the percentage for the progress bar
    progress_percent = 0
    if xp_needed > 0:
        progress_percent = int((profile.current_xp / xp_needed) * 100)
        
    context = {
        'xp_needed': xp_needed,
        'progress_percent': progress_percent,
    }
    return render(request, 'profiles/profiles.html', context)

@login_required
def equip_title_view(request):
    if request.method == 'POST':
        title_id = request.POST.get('title_id')
        if title_id:
            try:
                # Ensure the user actually owns the title before equipping it
                title = request.user.profile.unlocked_titles.get(id=title_id)
                request.user.profile.equipped_title = title
                request.user.profile.save()
            except Title.DoesNotExist:
                pass
    return redirect('profiles:profiles')
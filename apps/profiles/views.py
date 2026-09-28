from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    # request.user is passed automatically to the template by Django's context processors
    return render(request, 'profiles/profiles.html')
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from apps.profiles.models import Profile
from apps.user_settings.models import UserSettings

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if User.objects.filter(username=username).exists():
            return render(request, "register/register.html", {
                "error": "Username already exists."
            })
            
        # Create the base user account
        user = User.objects.create_user(username=username, password=password)
        
        # Initialize the gamified profile and settings linked to this user
        Profile.objects.create(user=user)
        UserSettings.objects.create(user=user)
        
        return redirect("login:login")
        
    return render(request, "register/register.html")
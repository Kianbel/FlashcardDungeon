from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from apps.profiles.models import Profile
from apps.user_settings.models import UserSettings


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            return render(request, "register/register.html", {
                "error": "Both an adventurer name and a password are required."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "register/register.html", {
                "error": "That adventurer name is already taken."
            })

        # Run Django's built-in password rules (length, too common, all numeric...)
        try:
            validate_password(password)
        except ValidationError as exc:
            return render(request, "register/register.html", {
                "error": " ".join(exc.messages)
            })

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user)
        UserSettings.objects.create(user=user)

        messages.success(request, "Guild registration complete! You may now enter.")
        return redirect("login:login")

    return render(request, "register/register.html")
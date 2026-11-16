from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect


@login_required
def settings_view(request):
    if request.method == 'POST':
        new_username = request.POST.get('username', '').strip()
        new_password = request.POST.get('new_password', '')
        changed = False

        # Update username only if it changed and nobody else has it
        if new_username and new_username != request.user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'That adventurer name is already taken.')
                return redirect('user_settings:user_settings')
            request.user.username = new_username
            request.user.save()
            changed = True

        # Update password if one was typed in
        if new_password:
            try:
                validate_password(new_password, request.user)
            except ValidationError as exc:
                for msg in exc.messages:
                    messages.error(request, msg)
                return redirect('user_settings:user_settings')
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # keeps the user logged in
            changed = True

        if changed:
            messages.success(request, 'Ledger updated successfully!')
        return redirect('user_settings:user_settings')

    return render(request, 'user_settings/user_settings.html')


@login_required
def delete_account_view(request):
    if request.method == 'POST':
        request.user.delete()  # cascades to Profile, Settings, and Dungeons
        return redirect('login:login')

    return redirect('user_settings:user_settings')
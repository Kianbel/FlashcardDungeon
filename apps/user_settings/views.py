from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

@login_required
def settings_view(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        
        # Update username if it was changed and isn't taken
        if new_username and new_username != request.user.username:
            request.user.username = new_username
            request.user.save()
            
        # Update password if the user typed one in
        if new_password:
            request.user.set_password(new_password)
            request.user.save()
            # This prevents the user from being logged out after a password change
            update_session_auth_hash(request, request.user) 
            
        messages.success(request, 'Ledger updated successfully!')
        return redirect('user_settings:user_settings')

    # We no longer need the mock user; Django automatically provides request.user to templates
    return render(request, 'user_settings/user_settings.html')

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        request.user.delete() # This cascades and deletes the Profile, Settings, and Dungeons
        return redirect('login:login') 
        
    return redirect('user_settings:user_settings')
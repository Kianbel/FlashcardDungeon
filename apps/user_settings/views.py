from django.shortcuts import render, redirect
from django.contrib import messages

# Mock classes (you need them here too so the template doesn't crash)
class MockProfile:
    def __init__(self):
        self.title = "Dungeon Master"
        self.level = 42

class MockUser:
    def __init__(self):
        self.username = "FlashcardHero"
        self.profile = MockProfile()

def settings_view(request):
    """Renders the settings page and fakes a form submission."""
    dummy_user = MockUser()
    
    if request.method == 'POST':
        messages.success(request, 'Settings updated successfully! (Mocked)')
        return redirect('user_settings:user_settings')

    return render(request, 'user_settings/user_settings.html', {'user': dummy_user})

def delete_account_view(request):
    """Simulates the account deletion route."""
    if request.method == 'POST':
        return redirect('login:login') 
        
    return redirect('user_settings:user_settings')
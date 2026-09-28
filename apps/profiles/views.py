from django.shortcuts import render

# Mock classes to fake the database
class MockProfile:
    def __init__(self):
        self.title = "Dungeon Master"
        self.level = 42
        self.total_recalls = 1337
        self.xp = 8500
        self.dungeons_cleared = 12

class MockUser:
    def __init__(self):
        self.username = "FlashcardHero"
        self.profile = MockProfile()

def profile_view(request):
    """Renders the profile page with fake data."""
    dummy_user = MockUser()
    return render(request, 'profiles/profiles.html', {'user': dummy_user})
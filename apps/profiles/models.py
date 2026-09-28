from django.contrib.auth.models import User
from django.db import models

class Title(models.Model):
    name = models.CharField(max_length=100) # e.g., "Novice Explorer"
    description = models.TextField(blank=True, null=True)
    required_level = models.IntegerField(default=1)
    sprite_asset_url = models.CharField(max_length=255, blank=True, null=True) # Path to 2D pixel art asset

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    
    # Gamification Stats
    level = models.IntegerField(default=1)
    current_xp = models.IntegerField(default=0)
    total_cards_memorized = models.IntegerField(default=0)
    
    # Title Relationships
    equipped_title = models.ForeignKey(
        Title, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='equipped_by'
    )
    unlocked_titles = models.ManyToManyField(
        Title, 
        related_name='unlocked_by', 
        blank=True
    )

    def __str__(self):
        return self.user.username
    
    def get_xp_for_next_level(self):
        # E.g., Level 1 needs 100 XP, Level 2 needs 282 XP, Level 3 needs 519 XP
        return int(100 * (self.level ** 1.5))

    def add_xp(self, gained_xp):
        self.current_xp += gained_xp
        leveled_up = False

        # Use a while loop in case they earn a massive amount of XP and gain multiple levels at once
        while self.current_xp >= self.get_xp_for_next_level():
            self.current_xp -= self.get_xp_for_next_level()
            self.level += 1
            leveled_up = True
            
        if leveled_up:
            self.check_title_unlocks()
            
        self.save()

    def check_title_unlocks(self):
        # Find titles where the required level is met, but the user doesn't own them yet
        new_titles = Title.objects.filter(
            required_level__lte=self.level
        ).exclude(
            id__in=self.unlocked_titles.all()
        )
        
        if new_titles.exists():
            self.unlocked_titles.add(*new_titles)
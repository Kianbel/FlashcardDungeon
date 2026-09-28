from django.contrib.auth.models import User
from django.db import models

class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    front_text = models.TextField() # The monster / question
    back_text = models.TextField()  # The weakness / answer
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Card: {self.front_text[:30]}"

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='sessions')
    enemies_killed = models.IntegerField(default=0)
    times_ran_away = models.IntegerField(default=0)
    xp_earned = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Dungeon Run: {self.deck.name} by {self.user.username}"

class CardReview(models.Model):
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE, related_name='reviews')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='reviews')
    is_successful = models.BooleanField() # True = Enemy Killed, False = Ran Away
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Success" if self.is_successful else "Fail"
        return f"Review {self.pk}: {status}"
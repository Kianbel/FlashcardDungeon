from django.contrib import admin
from .models import Deck, Card, StudySession, CardReview

admin.site.register(Deck)
admin.site.register(Card)
admin.site.register(StudySession)
admin.site.register(CardReview)
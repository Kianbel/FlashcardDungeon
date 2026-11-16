from django import forms
from .models import Deck, Card


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Data Structures'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What horrors await inside?'}),
        }


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['front_text', 'back_text']
        widgets = {
            'front_text': forms.Textarea(attrs={'rows': 2}),
            'back_text': forms.Textarea(attrs={'rows': 2}),
        }
"""Описание import"""
from django import forms
from .models import Word

class WordForm(forms.ModelForm):
    """Опиcание класса Модель Word
    Атрибуты:
        model = Word
        fields - Слово на английском и перевод
    """
    class Meta:
        model = Word
        fields = ['english_word', 'translation']

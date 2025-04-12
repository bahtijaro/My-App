"""Модель для хранения слов и их переводов"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Word(models.Model):
    """
    Атрибуты:
        user (ForeignKey): Связь с пользователем
        english_word (CharField): Слово на английском
        translation (CharField): Перевод
        created_at (DateTimeField): Дата создания записи
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    english_word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  # ТОЛЬКО auto_now_add

    def __str__(self):
        return f" {self.english_word} - {self.translation}"

    class Meta:

        verbose_name = 'Слово на анг. языке'
        verbose_name_plural = 'Слова на анг. языке'

"""Регистрация моделей в панели Django"""
from django.contrib import admin
from .models import Word

admin.site.register(Word)

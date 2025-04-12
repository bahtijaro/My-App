"""URL-маршруты для приложения main"""

from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
    # 1. начальный экран
    path('', views.welcome, name='welcome'),

    # 2. регистрация
    path('register/', views.register, name='register'),

    # 3. авторизация
    path('login/', views.login_view, name='login'),

    # 4. основная страница
    path('index/', views.index, name='index'),

    # 5.завершение работы, сменить пользователя
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 6.добавление слова
    path('add_word/', views.add_word, name='add_word'),

    # 7. удаление слова
    path('delete/<int:word_id>/', views.delete_word, name='delete_word'),

    # 8. редактирование слова
    path('word/<int:word_id>/edit/', views.edit_word, name='edit_word'),

    # 9. словарь (все слова)
    path('word_list/', views.word_list, name='word_list'),

    # 10. тестирование
    path('test/', views.start_test, name='start_test'),
]

"""Модуль представлений для приложения main.
Содержит обработчики запросов для:
- регистрация и авторизация пользователей;
- Работы со словарем (добавление, редактирование, удаление слов);
- Тестирования знаний слов;
"""

import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

from .forms import WordForm
from .models import Word

@login_required
def index(request):
    """основная страница (доступ только после авторизации)

    Returns:
        Рендер шаблона main/index.html
    """
    return render(request, 'main/index.html', {'user': request.user})

def welcome(request):
    """Отображает начальную страницу

    Returns:
        Рендер шаблона main/welcome.html
    """
    return render(request, 'main/welcome.html')


def register(request):
    """Отображает страницу регистрации новых пользователей

    Returns:
        Рендер шаблона main/welcome.html

    две ветки: либо регаемся либо авторизуемся
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    """Отображает страницу авторизации пользователей

    Returns:
        Рендер шаблона main/welcome.html

    2 ветка - доступ для авторизации существующего пользователя
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'main/login.html')


def logout_view(request):
    """Отображает страницу смены пользователя

    Returns:
        Рендер шаблона redirect

    выходим из авторизации и попадаем на начальный экран
    """
    logout(request)
    return redirect("")


@login_required
def add_word(request):
    """Отображает страницу добавить новые слова
    (доступ только после авторизации)

     """
    if request.method == "POST":
        form = WordForm(request.POST)
        # Проверка формы на валидацию
        if form.is_valid():
            english_word = form.cleaned_data['english_word']
            # ветка 1 - проверка на наличие уже имеющихся слов
            # в словаре, вывод сообщения и возврат на страницу
            if Word.objects.filter(english_word__iexact=english_word).exists():
                messages.error(request, 'Это слово уже есть в Словаре!, введите другое слово!')
                return render(request, 'main/add_word.html', {'form': form})
            # ветка 2 - сохраняем слово  с проверкой добавления
            # пользователя (надо знать кто какое слово ввел)
            word = form.save(commit=False)
            word.user = request.user
            word.save()
            # messages.success(request, 'Cлово успешно добавлено в Словарь!')
            return redirect('word_list')
    form = WordForm()
    return render(request, 'main/add_word.html', {'form': form})


@login_required
def word_list(request):
    """Отображает страницу со словарем
    (доступ только после авторизации)
    с сортировкой по анг. словам (доступ только после авторизации)
    Returns:
    Рендер шаблона main/word_list.html
    """
    words = Word.objects.all().order_by('english_word')
    return render(request, 'main/word_list.html', {'words': words})

def delete_word(request, word_id):
    """Возможность удаления слов из словаря (удаление только слов,
    которые ввел конкретный пользователь или Админ)
    """
    word = get_object_or_404(Word, id=word_id)
    if not (word.user == request.user or request.user.is_superuser):
        raise Http404("Слово не найдено или у вас нет прав")
    word.delete()
    return redirect('word_list')


@login_required
def edit_word(request, word_id):
    """редактирование слов из словаря (редактирование только слов,
    которые ввел конкретный пользователь или Админ)
    """
    word = get_object_or_404(Word, id=word_id)
    # ветка 1 - доступ отсутствует
    if not (word.user == request.user or request.user.is_superuser):
        messages.error(request, 'У вас нет прав для редактирования этого слова')
        return redirect('word_list')
    # ветка 2 - доступ есть
    if request.method == "POST":
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            english_word = form.cleaned_data['english_word']
            # ветка 1 - проверка на наличие уже имеющихся слов в словаре,
            # повторяет логику, что и для добавления новых слов
            if Word.objects.filter(english_word__iexact=english_word).exists():
                messages.error(request, 'Это слово уже есть в Словаре!, введите другое слово!')
                return render(request, 'main/add_word.html', {'form': form})
            # ветка 2 - сохраняем слово  с проверкой добавления
            # пользователя (надо знать кто какое слово ввел
            word = form.save(commit=False)
            word.user = request.user
            form.save()
            messages.success(request, 'Слово успешно обновлено!')
            return redirect('word_list')
    else:
        form = WordForm(instance=word)
    return render(request, 'main/edit_word.html', {'form': form})



@login_required
def start_test(request):
    """тестирование и проверка пользователя на знание словаря
    Returns: Страница теста, предупреждения или результатов
    """

    if Word.objects.count() < 10:
        # Ветка 1: Проверяем хватает ли нам в базе слов для теста
        # Слов не достаточно, то открываем страницу с предупреждением
        return render(request, 'main/test_warning.html', {
            'current_words': Word.objects.count(),
            'required_words': 10
        })
    # Ветка 2: Слов в словаре достаточно
    # (в рандоме все слова .all независимо от пользователя)
    if request.method == 'POST':
        # Получаем ID слов из сессии, которые были показаны текущему пользователю
        test_words_ids = request.session.get('test_words_ids', [])
        test_words = Word.objects.filter(id__in=test_words_ids)

        # Если слова не найдены (или сессия устарела), перенаправляем на тест
        if len(test_words) != 10:
            return redirect('main/start_test.html')

        correct = 0  # кол-во правильных ответов
        results = [] # сюда будем записывать результат теста
        # проходим по словам и сравниваем, че нам
        # пользователь написал, с тем что в переводе, учет lower символов
        for word in test_words:
            user_answer = request.POST.get(f'word_{word.id}', '').strip()
            is_correct = (user_answer.lower() == word.translation.lower())
            # собираем результат: слово, ответ пользователя и верно/неверно
            results.append({
                'word': word,
                'user_answer': user_answer, #ответ пользователя
                'is_correct': is_correct, #верный/неверный ответ
                'correct_translation': word.translation  #верный перевод
                })
            # считаем, сколько слов верных ввел пользователь
            if is_correct:
                correct += 1
        # считаем процент верных ответов
        percent = int((correct / 10) * 100)
        # по завершении тестов переход на страницу результатов теста
        return render(request, 'main/test_results.html', {
                'results': results,
                'correct': correct,
                'percent': percent
        })

    # GET-запрос: генерируем новые ВСЕ слова и сохраняем их ID в сессии
    all_words = Word.objects.all()
    test_words = random.sample(list(all_words), 10)
    request.session['test_words_ids'] = [word.id for word in test_words]
    return render(request, 'main/test.html', {'words': test_words})

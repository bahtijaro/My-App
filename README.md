# Тренажер для изучения английского языка
Проект на базе Python плюс фреймворк Django.
Функциональность приложения:
1. Добавление английских слов в словарь,включая перевод;
2. Возможность редактирования текста анг. слов и переводов к ним, а также удаление слов (редактировать и удалять слова можно только те, которые пользователь сам ввел). Админ может удалять слова у всех пользователей;
3. Просмотр всех слов в словаре для всех пользователей;
4. Тестирование на знание слов на английском языке (тест состоит из 10 случайных слов) с последующим выводом результатов тестирования.

## Как использовать
1. Скачать этот репозиторий или клонировать его;
2. При открытии в PyCharm необходимо подтвердить создание виртуального окружения:
   ![image](https://github.com/user-attachments/assets/4330cb8e-c88c-4621-9599-4a36fe2bc357)
3. После нажатия подтверждения (кнопка "ОК") проконтролировать уставку требуемых библиотек;
4. Так как .env файл (где располагается secret key) отсутствует в репозитории, то необходимо в терминале запустить следующую команду copy .env.example .env (файл example .env присутствует в репозитории)
   и проконтролировать создание файл .env;
5. Далее необходимо сгенерировать secret key при помощи команды (запускать ее находясь в корне приложения) python -c "from django.core.management.utils import get_random_secret_key; print(f'SECRET_KEY={get_random_secret_key()}')"
6. Открыть файл .env и в поле SECRET_KEY ввести ранее сгенерированный secret key или, т.к. проект учебный, использовать тот, который указан в файле .env;
7. Выполнить миграцию при помощи команды  python manage.py migrate;
8. Выполнить создание суперюзера при помощи команды python manage.py createsuperuser (логин admin, email - пропустить, пароль - вести и придумать);
9. Запустить сервер при помощи команды python manage.py runserver;
10. После появления в терминале сообщения о старте сервера http://127.0.0.1:8000, необходимо кликнуть по указанному адресу и проконтролировать присутствие начальной страницы проекта со авторизацией и регистрацией.

## Адреса основные (все html-страницы см. в templates)
1. http://127.0.0.1:8000/admin/ - логинимся используя данные созданного superuser;
2. http://127.0.0.1:8000/ - стартовая страница, регистрация нового пользователя или авторизация существующего;
3. http://127.0.0.1:8000/index - первый кадр с описанием проекта;
4. http://127.0.0.1:8000/add_word/ - страница, на которой можно добавить слова в словарь;
5. http://127.0.0.1:8000/word_list/ - страница, на которой отображаются введенные пользователями слова и переводы к ним;
6. http://127.0.0.1:8000/test/ - страница, на которой отображаются данные по тестированию пользователя;

## Для проверки качество кода необходимо использовать pylint:
Файл .pylintrc уже присутствует в проекте. Для работы с pylint необходимо выполнить команды в терминале:
1. pip install pylint
2. pip install pylint-django

Запуск проверки через терминал:
1. pylint main/ --load-plugins pylint_django

Бахтияров Р.А. 13.04.2025 г.
Проект Python + Django для "Модуль 3. Создание Web-сервисов на Python" Пуск МФТИ.

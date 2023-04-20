# Файл окружения.
1. Создайте файл .env в корневой папке
2. Заполните .env как показано в файле .env.example
# Разворачивание окружения.
  Из корня проекта запустить терминал и выполнить команды:
1. ~docker-compose build
2. ~docker-compose up -d
3. В браузере выполнить запрос http://localhost.8000/
  Откроется приветственная страница проекта
4. ~docker-compose down для завершения работы

Для входа в админку
1. ~docker-compose build
2. ~docker-compose up -d
3. ~docker-compose exec wed python manage.py migrate
4. ~docker-compose exec wed python manage.py createsuperuser
5. http://localhost.8000/admin/

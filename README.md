Hotel Booking System
Этот проект представляет собой систему бронирования отелей, созданную с использованием Django REST.

Шаги для поднятия проекта.

1)Клонируйте репозиторий проекта
git clone https://github.com/razoterhovhannisyan/hotel-booking-system.git

2)Перейдите в директорию проекта:
cd hotel-booking-system

3)Создайте виртуальное окружение:
python -m venv venv

4)Активируйте виртуальное окружение:
env\Scripts\activate

5)Установите зависимости проекта(requirements.txt):
pip install -r requirements.txt

6)Примените миграции базы данных
python manage.py migrate

7)Создайте суперпользователя
python manage.py createsuperuser


8)Запустите сервер разработки
python manage.py runserver

Тестирование:

Тесты для моделей(models):
python manage.py test bookingapp.tests.test_models

Тесты для представлений:(views)
python manage.py test bookingapp.tests.test_views

Тесты для URL:
python manage.py test bookingapp.tests.test_urls


Все API эндпоинты доступны по адресу http://127.0.0.1:8000/

Аутентификация: Для доступа к защищенным эндпоинтам API необходимо аутентифицироваться. Используйте токен, полученный при авторизации, для выполнения запросов.

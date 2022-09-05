# Foodgram React

[![Django-app workflow](https://github.com/Hastred45/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/Hastred45/yamdb_final/actions/workflows/yamdb_workflow.yml)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=ffffff&color=043A6B)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=ffffff&color=043A6B)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=043A6B)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=ffffff&color=043A6B)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=ffffff&color=043A6B)](https://gunicorn.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=ffffff&color=043A6B)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=ffffff&color=043A6B)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=ffffff&color=043A6B)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=ffffff&color=043A6B)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=ffffff&color=043A6B)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=ffffff&color=043A6B)](https://cloud.yandex.ru/)

## Описание

Сервис, в котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Также у пользователей есть возможность создавать список продуктов, которые нужно купить для приготовления выбранных блюд, и загружать его в формате PDF.

В рамках учебного проекта был разработан backend сервиса и настроен CI/CD.

## Доступ

Проект запущен на сервере и доступен по адресам:

http://hastred.sytes.net/admin

http://hastred.sytes.net/recipes

http://130.193.53.106/admin (если временный домен откажется работать)

http://130.193.53.106/recipes

Доступ для ревью:

логин для админки - has
почта для сайта - has@has.as
пароль - 73501505has

## Для запуска на собственном сервере:
1. Скопируйте из репозитория файлы, расположенные в директории infra:
    - docker-compose.yml
    - nginx.conf
2. На сервере создайте директорию infra;
3. Поместите в неё файлы:
    - docker-compose.yml
    - nginx.conf
    - .env (пустой)
4. Файл .env должен быть заполнен следующими данными:
```
SECRET_KEY=<КЛЮЧ>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<ИМЯ БАЗЫ ДАННЫХ>
POSTGRES_USER=<ИМЯ ЮЗЕРА БД>
POSTGRES_PASSWORD=<ПАРОЛЬ БД>
DB_HOST=db
DB_PORT=5432
```

5. В директории infra следует выполнить команды:
```
docker-compose up -d
docker-compose exec Django python manage.py makemigrations
docker-compose exec Django python manage.py migrate
docker-compose exec Django python manage.py collectstatic --no-input
```

6. Для создания суперпользователя, выполните команду:
```
docker-compose exec Django python manage.py createsuperuser
```

7. Для добавления ингредиентов в базу данных, выполните команду:
```
docker-compose exec Django python manage.py add_data ingredients.csv tags_ingr_ingredient
```
После выполнения этих действий проект будет запущен в трех контейнерах (Django, PostgreSQL, nginx) и доступен по адресам:

- Главная страница: http://<ip-адрес>/recipes/
- API проекта: http://<ip-адрес>/api/
- Admin-зона: http://<ip-адрес>/admin/
8. Теги вручную добавляются в админ-зоне в модель Tags;
9. Проект запущен и готов к регистрации пользователей и добавлению рецептов.

### Автор
Sergey Osetorov

hastred45@yandex.ru

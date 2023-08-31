# Database application
Приложение "Database application" - это приложение для получения вакансий выбранных работодателей из API сайта hh.ru и сохранения их в базу данных. С помощью приложения можно из базы данных получить список всех компаний и количество вакансий у каждой компании, список всех вакансий, среднюю зарплату по вакансиям, вакансии с зарплатой выше средней, поиск вакансий по ключевым словам.
# Установка
## Для установки проекта необходимо:
- Склонировать репозиторий с помощью команды git clone https://github.com/samwance/cw_5
- Установить пакетный менеджер Poetry с помощью команды pip install poetry
- Перейти в папку проекта cd course_work_5
- Установить необходимые зависимости с помощью команды poetry install
- В папке проекта изменить файл database.ini по образцу:
```
[postgresql]
host=localhost
user=<имя_пользователя>
password=<пароль>
port=<порт>
```
  
# Использование
Для запуска приложения необходимо выполнить команду python main.py.

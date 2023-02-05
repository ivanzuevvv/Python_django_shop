# Django магазин
Это индивидуальный дипломный проект по разработке бек-энда интернет-магазина, 
с использованием фреймворка Python Django.

## Установка

* Необходимо скопировать все содержимое репозитория в отдельный каталог.

* Установить все связи из `requirements.txt`

```
python pip install -r requirements.txt
```

* Провести миграции:

```
python manage.py makemigrations
python manage.py migrate
```

## Для тестирования и для того, что бы составить представление о работе программы

* Загрузите фикстуры:

```
python manage.py loaddata fixtures/fixture_data.json
```

* В фикстурах суперпользователь: 
**admin@admin.an** 
пароль: **admin** 

* Остальные пользователи:
- 'zea@crid.ru',
- 'peter@cho.za',
- 'chtoto@za.pochta',
- 'valid@me.co',
- 'sova@cho.za',
- 'ulyba@cho.za',
- '123@cho.za',
- 'kot@na.oborot'
* Пароль для любого: **1234**

## Запуск

* Для запуска сайта воспользуйтесь командной:

```
python manage.py runserver
```
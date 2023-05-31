# Общая часть

## Что из себя представляет проект
Предтаавляет собой подключаемое django-приложение. Берет на себя все что связано с отобоажением страниц, а обращение 
за данными происходит по API, который необходимо реализовать в ходе выполения задания дипломного проекта.

## Контракт для API
Названия роутов и ожидаемую структуру ответа от API endpoints можно найти в `diploma-frontend/swagger/swagger.yaml`. 
Для более удобного просмотра swagger-описания рекомендуется использовать возможности gitlab:
![image](./gitlab-swagger.png)

## Подключение пакета
1. Собрать пакет: в директории diploma-frontend выполнить команду python setup.py sdist
2. Установить полученный пакет в виртуальное окружение: `pip install diploma-frontend-X.Y.tar.gz`. X и Y - числа, они могут изменяться в зависимости от текущей версии пакета.
3. В `settings.py` дипломного проекта подключить приложение:
```python
INSTALLED_APPS = [
        ...
        'frontend',
    ]
```
4. В `urls.py` добавить:
```python
urlpatterns = [
    path("", include("frontend.urls")),
    ...
]
```
Если запустить сервер разработки: `python manage.py runserver`, то по адресу `127.0.0.1:8000` должна открыться стартовая страница интернет-магазина:
![image](./root-page.png)

# Детали подключаемого приложения `frontend` (Для проверяющих преподавателей)
Приложение служит только для отрисовки шаблонов из `templates/frontend`, поэтому в `urls.py` напрямую 
используются `TemplateView` из стандартной поставки Django.

В качестве frontend фреймворка был использован Vue3, который подключается в базовом шаблоне `templates/frontend/base.html`:
```html
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
```
JS скрипт `static/frontend/assets/js/app.js` содержит реализацию Vue объекта, а все остальные JS скрипты из 
директории `static/frontend/assets/js` реализуют объекты примеси для соответствующей страницы проекта.

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

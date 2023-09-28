# Интернет-магазин Megan
Проект интернет-магазина, написанный на python с использованием фреймворка Django.

## Оглавление
1. [Инструменты](#Инструменты)
2. [Возможности](#Функционал)
3. [Установка](#Установка)
4. [Скриншоты](#Скриншоты)

## Инструменты
* **Python** (3.11);
* **Django** (Wev Framework);
* **PostgreSQL** (database);
* **Redis** (message broker for celery);
* **Celery** (background tasks);
* **Flower** (tracking background tasks);
* **logging** (logging);

[//]: # (* **Pytest** &#40;tests&#41;;)
* **Docker** and **Docker Compose** (containerization);
* **Gunicorn** (WSGI HTTP Server);
* **Nginx** (Web Server).

## Функционал
*Приложение позволяет*:
- Создавать товары различных категорий (в т.ч. вложенных);
- Оставлять комментарии к товарам;
- Выполнять поиск, фильтровать и сортировать товары по различным параметрам;
- Регистрироваться и создавать профиль с отслеживанием истории просмотров и покупок;
- Добавлять товары в корзину, удалять и менять кол-во товара в корзине 
(как для авторизованных, так и неавторизованных пользователей);
- Оформлять заказ с вводом и оплаты заказа по фиктивным данным (имитация оплаты заказа в фоне при помощи Celery).

## Установка

1. Копируем содержимое репозитория в отдельный каталог:
```
git clone https://github.com/FreemaHG/django-shop.git
```
2. Переименовываем файл "**.env.template**" в "**.env**", при необходимости можно задать свои параметры.

3. Собираем и запускаем контейнеры с приложением. В терминале в общей директории (с файлом "docker-compose.yml") 
вводим команду:
```
docker-compose up -d
```

4. Сбор статических файлов для последующей обработки сервером nginx:
```
docker-compose exec app python3 -m app.manage collectstatic --noinput
```

5. Применяем миграции (создаем БД с зависимостями):
```
docker-compose exec app python3 -m app.manage migrate
```

6. Загрузка демонстрационных данных (опционально):
```
docker-compose exec app python3 -m app.manage loaddata app/fixtures/test-data.json
```

Добавятся записи с товарами, комментариями, заказами и суперпользователем:
  - логин: admin; 
  - пароль: admin.

7. Создание суперпользователя (опционально):
```
docker-compose exec app python3 -m app.manage createsuperuser
```
Приложение запускается автоматически и доступно по адресу: `http://<domen>/`

Админка: `http://<domen>/admin/`

**ВАЖНО**: домен задается в файле **.env** в переменной окружения **DOMEN_HOST**.

## Скриншоты
![](/screen/2023-06-25_14-54-43.jpg)
![](/screen/2023-06-25_14-57-10.jpg)
![](/screen/2023-06-25_14-58-25.jpg)
![](/screen/2023-06-25_14-59-44.jpg)
![](/screen/2023-06-25_15-00-24.jpg)
![](/screen/2023-06-25_15-01-24.jpg)
![](/screen/2023-06-25_15-05-02.jpg)
![](/screen/2023-06-25_15-05-29.jpg)
![](/screen/2023-06-25_15-07-08.jpg)
![](/screen/2023-06-25_15-07-33.jpg)
![](/screen/2023-06-25_15-08-04.jpg)
![](/screen/2023-06-25_15-08-32.jpg)

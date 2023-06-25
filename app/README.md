# Django магазин
Проект интернет-магазина, написанный на Python с использованием фреймворка Django.

## Оглавление
1. [Возможности](#Функционал)
2. [Установка](#Установка)
3. [Скриншоты](#Скриншоты)

## Функционал
*Приложение позволяет*:
- Создавать товары различных категорий (в т.ч. вложенных);
- Оставлять комментарии к товарам;
- Выполнять поиск, фильтровать и сортировать товары по различным параметрам;
- Регистрироваться и создавать профиль с отслеживанием истории просмотров и покупок;
- Добавлять товары в корзину, удалять и менять кол-во товара в корзине 
(как для авторизованных, так и неавторизованных пользователей);
- Оформлять заказ с вводом и оплаты заказа по фиктивным данным;

## Установка

* Необходимо скопировать все содержимое репозитория в отдельный каталог.
* устанавливаем все библиотеки из `requirements.txt` командой:

```
pip install -r requirements.txt
```

* Вводим след. команды в терминале из папки проекта:

```
python manage.py makemigrations
python manage.py migrate
```

* Создаем суперпользователя командой:

```
python manage.py createsuperuser
```

* Теперь можно зайти в админку проекта, по адресу `http://127.0.0.1:8000/admin/`.

* Для загрузки фикстур с тестовыми данными используйте команду:

```
python manage.py loaddata fixtures/test-data.json
```

## Скриншоты
![Alt-текст](https://downloader.disk.yandex.ru/preview/b9b0bc4607921fcc1615579bf64a162adbbc907b4864829be3b90f58c4309c8c/649867e2/e2AlzIJ0la5dmWHEERLbnZ5FTpeUwU0LgOtIIU7kZ8inf6QZy9hcv075L1S5v0Zaq7aP8uGZe4ZeETM-SGW0hg%3D%3D?uid=0&filename=2023-06-25_14-54-43.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1024x1024)

![Alt-текст](https://downloader.disk.yandex.ru/preview/68d51e3b55cb74dd1327387b7507691a24d470a09d8be82bcbc16c0a87654321/64986a44/UMwGaICrJHqqlUtli-g_8b-cWrkwgXzSLgEib-Q0Paax_XNfnenunoW5CA8iQzGyVMvcDnjEsb1n49eKMGnMsQ%3D%3D?uid=0&filename=2023-06-25_14-57-10.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1024x1024)

![Alt-текст](https://downloader.disk.yandex.ru/preview/a03817b58cd507b78d9fdf5c12f23c78bccae0177fc49b73dba047a4a561eda2/64986ad9/9kyltEwJS6clUTqtgLpOkZ5FTpeUwU0LgOtIIU7kZ8g15NLYfSkloORWZZCnfL52VUyZuWwqrZLVS44pziFXEw%3D%3D?uid=0&filename=2023-06-25_14-58-25.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1024x1024)

![Alt-текст](https://downloader.disk.yandex.ru/preview/7a030745145c2c2e52541bdc920b095e4fb64ff7423a7a57da97a04e73febeeb/64986b04/BBG6nB9kIBtbaFy6GTwl555FTpeUwU0LgOtIIU7kZ8iLca8XBWnVTlwDkC1KAuYycbf1Wvc61yd16wGK80mTrQ%3D%3D?uid=0&filename=2023-06-25_14-59-44.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1024x1024)

![Alt-текст](https://downloader.disk.yandex.ru/preview/1cc0c415a1e5dde37665dd75d1247741c5a65bbb5f50d4c79224f12f0d37ad58/64986b30/gclT0JWXMlFR8uNjGIg1h55FTpeUwU0LgOtIIU7kZ8iM7jGqFOtz7fv68e_7VZoGiPAWmBdcXIlgxcqq_2uTew%3D%3D?uid=0&filename=2023-06-25_15-00-24.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1024x1024)

![Alt-текст](https://downloader.disk.yandex.ru/preview/95b9a1353398c13902bc12936b0ba4f59116ed1ba92f85a87d3d4a12ca9499cb/64986b66/9RtYOiGtU-hQUKvJDe9h_WtfWTk_35l35rePTvUihO1ex1uv2oJ7Y8_LBiBN8Ar7_hlZjRTp9d9te7DbHO-hBg%3D%3D?uid=0&filename=2023-06-25_15-01-24.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1024x1024)

![Alt-текст](https://downloader.disk.yandex.ru/preview/e7e2be0deb052ce0c5ceb08163455efb6803f698d2eaee2460884c9c4b92ec0f/64986b93/aJ6Lfh50JIPnol26FX4ne7-cWrkwgXzSLgEib-Q0Paaw6qqCEi6Vl1yMgBbNh27QnMpYpRiR67lrvY37OaH8KA%3D%3D?uid=0&filename=2023-06-25_15-05-02.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1024x1024)

![Alt-текст](https://downloader.disk.yandex.ru/preview/b823c0373561741505c2125a889a238c15dcd47a5a258595f9933cc14ee942e2/64986bb6/Cs9bww2JgOTEYCbb1o_h6r-cWrkwgXzSLgEib-Q0PaY0d2B6esLlP1VnOKoi7aDhIdRdu_G1tBu7gVGyPa5h5g%3D%3D?uid=0&filename=2023-06-25_15-05-29.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1024x1024)

![Alt-текст](https://downloader.disk.yandex.ru/preview/c6769763767621641d0948df66352424aec0d3baf597f0d8775aa52e50978602/64986bd9/a36YdzuwRUhB6sXG1k8-CcKG0fEuvtEsSOB9lfcXCl9hjnsqaf-XDt5F8NeDUYnUIlvdhtuMAS5toHwQE-VNRQ%3D%3D?uid=0&filename=2023-06-25_15-07-08.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1024x1024)

![Alt-текст](https://downloader.disk.yandex.ru/preview/2c163db7baed499e19ffcf690931b9ccd0ef1daf3b49ddf6b565db31c032d759/64986bf9/haFiws-zn6jhiEkSbUihyJ5FTpeUwU0LgOtIIU7kZ8g9YC6lohymgNRJHI0UM_ltsSuHsmy2z-DbhcquiK-cbg%3D%3D?uid=0&filename=2023-06-25_15-07-33.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1024x1024)

![Alt-текст](https://downloader.disk.yandex.ru/preview/9473784714b197b2d041617958f44f3948470e40a9568a8e28c3809ffab2a16c/64986c18/rUSXHz5oaxFK-RxeoVqwS55FTpeUwU0LgOtIIU7kZ8jxDo-LpCGui-WdLCsDNqvcMf4kdYA_KCNsnen01sbAEg%3D%3D?uid=0&filename=2023-06-25_15-08-04.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1024x1024)

![Alt-текст](https://downloader.disk.yandex.ru/preview/cdaca6b28f25af7c8d6f6d67adb1b5457b34590e859ec253517bdd83d5fab9f1/64986c36/0EK2rGuEj5O9ja257_MQYWtfWTk_35l35rePTvUihO1Nat0dG3E4eJ1poffTeb-CEPN809RF9vW0ITPRbykZgA%3D%3D?uid=0&filename=2023-06-25_15-08-32.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1024x1024)

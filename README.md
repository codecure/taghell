Сервис для выдачи листинга фотографии по набору тегов привязанных к ним с сортировкой.

## Установка
$ virtualenv taghell
$ . taghell/bin/activate
$ pip install -r requirements.txt
$ mysql -uUSER -hHOST -p -e 'CREATE DATABASE `taghell` CHARACTER SET utf8 COLLATE utf8_general_ci;'
$ mysql -uUSER -hHOST -p taghell < taghell.sql
$ python fill_db.py  # Займет продолжительное время


## Запуск
$ python app.py

## Запросы
http://127.0.0.1:5000/tags
http://127.0.0.1:5000/?tag=tag1&tag=tag2
http://127.0.0.1:5000/page/2?tag=tag1&tag=tag2
http://127.0.0.1:5000/page/2?tag=tag1&tag=tag2&sort=created_at
http://127.0.0.1:5000/page/2?tag=tag1&tag=tag2&sort=likes&sort_direction=asc

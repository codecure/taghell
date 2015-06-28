Сервис для выдачи листинга фотографий по набору тегов, привязанных к ним, и сортировкой.

## Установка
    $ virtualenv taghell
    $ . taghell/bin/activate
    $ pip install -r requirements.txt --allow-external mysql-connector-python
    $ mysql -uUSER -hHOST -p -e 'CREATE DATABASE `taghell` CHARACTER SET utf8 COLLATE utf8_general_ci;'
    $ mysql -uUSER -hHOST -p taghell < taghell.sql
    $ echo -e "DB_USER='your_db_user'\nDB_PASSWORD='your_db_password'\n" > config_local.py
    $ python fill_db.py  # Займет продолжительное время


## Запуск
    $ python app.py

## Запросы
    http://127.0.0.1:5000/tags
    http://127.0.0.1:5000/?tag=tag1&tag=tag2
    http://127.0.0.1:5000/page/2?tag=tag1&tag=tag2
    http://127.0.0.1:5000/page/2?tag=tag1&tag=tag2&sort=created_at
    http://127.0.0.1:5000/page/2?tag=tag1&tag=tag2&sort=likes&sort_direction=asc

## Пример ответа
    {
    "photos": [
        {
            "src": "http://site/image.jpg",
            "created_at": "2016-02-18 15:57:08",
            "likes": 9,
            "tags": "tag1, tag2"
        },
        ...
    ],
    "pagination": {
        "has_next": true,
        "has_prev": false,
        "pages": 100,
        "page": 1,
        "items": [
            {
                "url": "http://127.0.0.1:5000/?tag=tag1&tag=tag2",
                "page": 1
            },
            {
                "url": "http://127.0.0.1:5000/page/2?tag=tag1&tag=tag2",
                "page": 2
            },
            {
                "url": "http://127.0.0.1:5000/page/3?tag=tag1&tag=tag2",
                "page": 3
            },
            {
                "url": "http://127.0.0.1:5000/page/4?tag=tag1&tag=tag2",
                "page": 4
            },
            {
                "url": "http://127.0.0.1:5000/page/5?tag=tag1&tag=tag2",
                "page": 5
            },
            {
                "url": null,
                "page": "..."
            },
            {
                "url": "http://127.0.0.1:5000/page/99?tag=tag1&tag=tag2",
                "page": 99
            },
            {
                "url": "http://127.0.0.1:5000/page/100?tag=tag1&tag=tag2",
                "page": 100
            }
        ]
    },
    "time": "0.262s"
    }

# coding: utf-8
import random
import string
from datetime import timedelta, datetime

import mysql.connector as mariadb

from config import DB_USER, DB_PASSWORD, DB_NAME

MAX_PHOTOS = 10 ** 6
MAX_USERS = 10 ** 4
MAX_TAGS = 10 ** 2
TAGS_PER_PHOTO = (3, 7)
START_DATE = datetime.now()
END_DATE = START_DATE + timedelta(days=365)

mariadb_connection = mariadb.connect(user=DB_USER, password=DB_PASSWORD,
                                     database=DB_NAME)
cursor = mariadb_connection.cursor()

photo_urls = []
with open('test-photo.csv') as tp:
    for row in tp:
        photo_urls.append(row.split(';')[1].strip('"'))
photo_urls = photo_urls[1:]

generate_tag = lambda a: ''.join(
    [random.choice(string.letters) for _ in range(a)])


def random_date(start, end):
        return start + timedelta(
            seconds=random.randint(0, int((end - start).total_seconds())))

# insert tags in table
for _ in xrange(MAX_TAGS):
    tag_sql_str = "INSERT INTO tag (name) VALUES (%s)"
    cursor.execute(tag_sql_str, (generate_tag(7), ))
    mariadb_connection.commit()

# select tags names
cursor.execute('SELECT name FROM tag')
tag_names = [t[0] for t in cursor.fetchall()]

for _ in xrange(MAX_PHOTOS):
    photo_sql_str = (
        "INSERT INTO photo (user_id, src, created_at, likes, tags) " +
        "VALUES (%s, %s, %s, %s, %s)")

    tag_str = ','.join(random.sample(tag_names, 5))
    cursor.execute(photo_sql_str, (random.randint(1, MAX_USERS),
                                   random.choice(photo_urls),
                                   random_date(START_DATE, END_DATE),
                                   random.randint(1, 111),
                                   tag_str))
    mariadb_connection.commit()

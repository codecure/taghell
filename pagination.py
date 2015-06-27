# coding: utf-8
from math import floor
import mysql.connector as mariadb

from config import PER_PAGE, COUNT_QUERY, SELECT_QUERY, TAGS_QUERY


class Pagination(object):
    def __init__(self):
        self.db_conn = mariadb.connect(user='root', password='',
                                       database='taghell')
        self.cursor = self.db_conn.cursor(buffered=True)

    def total_pages(self, tags_list):
        params = tags_list + [len(tags_list)]

        self.cursor.execute(
            COUNT_QUERY % (self.placeholders(tags_list), '%s'), params)

        total_pages = self.cursor.fetchone()[0]

        return int(floor(total_pages / float(PER_PAGE)))

    def tags_list(self):
        self.cursor.execute(TAGS_QUERY)
        return [t[0] for t in self.cursor.fetchall()]

    def iter_pages(self, pages, page, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0

        for num in xrange(1, pages + 1):
            if num <= left_edge or \
                (num > page - left_current - 1 and
                 num < page + right_current) or \
                    num > pages - right_edge:
                if last + 1 != num:
                    yield '...'
                yield num
                last = num

    def placeholders(self, tags_list):
        return ', '.join(['%s'] * len(tags_list))

    def get_photos(self, page=1, tags_list=None, sort=None,
                   sort_direction=None):
        params = tags_list + [len(tags_list), page * PER_PAGE]

        sort_str = ''
        if sort:
            sort_str = 'ORDER BY p.%s %s'
            if sort_direction:
                sort_str = sort_str % (sort, sort_direction)
            else:
                sort_str = sort_str % (sort, 'DESC')

        self.cursor.execute(
            SELECT_QUERY % (
                self.placeholders(tags_list), '%s', sort_str, '%s'), params)

        result = []
        for c in self.cursor:
            result.append(dict(
                src=c[0],
                created_at=str(c[1]),
                likes=c[2],
                tags=c[3]
            ))

        return result

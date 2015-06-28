# coding: utf-8
from math import ceil
import mysql.connector as mariadb

from config import (PER_PAGE, COUNT_QUERY, SELECT_QUERY,
                    TAGS_QUERY, MATCH_TAG, NOT_MATCH_TAG)


class Pagination(object):
    def __init__(self):
        self.db_conn = mariadb.connect(user='root', password='',
                                       database='taghell')
        self.cursor = self.db_conn.cursor(buffered=True)

    def build_query_where(self, tags_list):
        db_tags = [t for t in self.tags_list() if t[0] in tags_list]

        tag_matches = []
        tag_not_matches = []

        for tag in tags_list:
            for t in db_tags:
                if t[0] == tag:
                    if t[1] == 0:
                        tag_matches.append(MATCH_TAG % tag)
                    else:
                        tag_not_matches.append(NOT_MATCH_TAG % tag)

        query = []
        if tag_matches:
            for tm_cnt in xrange(len(tag_matches)):
                if tm_cnt > 0:
                    query.append(' and %s' % tag_matches[tm_cnt])
                else:
                    query.append(' %s' % tag_matches[tm_cnt])
            for tnm in tag_not_matches:
                query.append(' and %s' % tnm)

            return ''.join(query)
        return None

    def total_pages(self, tags_list):
        where_part = self.build_query_where(tags_list)
        self.cursor.execute(COUNT_QUERY % where_part)

        total_results = self.cursor.fetchone()[0]

        return int(ceil(total_results / float(PER_PAGE)))

    def tags_list(self):
        self.cursor.execute(TAGS_QUERY)
        return self.cursor.fetchall()

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

    def get_sort(self, sort=None, sort_direction=None):
        sort_str = ''
        if sort:
            sort_str = 'ORDER BY %s %s'
            if sort_direction:
                sort_str = sort_str % (sort, sort_direction)
            else:
                sort_str = sort_str % (sort, 'DESC')
        return sort_str

    def get_photos(self, tags_list, page=1, sort=None,
                   sort_direction=None):
        where_part = self.build_query_where(tags_list)

        if not where_part:
            return None

        sort_str = self.get_sort(sort, sort_direction)

        self.cursor.execute(
            SELECT_QUERY % (where_part, sort_str, PER_PAGE, page * PER_PAGE))

        result = []
        for c in self.cursor:
            result.append(dict(
                src=c[0],
                created_at=str(c[1]),
                likes=c[2],
                tags=c[3]
            ))

        return result

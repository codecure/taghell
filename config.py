# coding: utf-8
DB_NAME = 'taghell'
DB_USER = 'root'
DB_PASSWORD = ''

PER_PAGE = 20

COUNT_QUERY = """
    select count(1)
    from (
        select id
        from photo
        where %s
    ) as tmp
"""

MATCH_TAG = "match (tags) against ('%s')"
NOT_MATCH_TAG = "not match (tags) against ('%s')"

SELECT_QUERY = """
    select src, created_at, likes, tags
    from photo
    where %s
    %s
    limit %s offset %s
"""

TAGS_QUERY = "SELECT name, off FROM tag;"

try:
    from config_local import *
except ImportError:
        pass

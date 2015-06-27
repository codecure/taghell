# coding: utf-8

PER_PAGE = 20

COUNT_QUERY = """
    SELECT COUNT(1)
    FROM (
        SELECT p.id
        FROM tagmap tm, photo p, tag t
        WHERE tm.tag_id = t.id
        AND (t.name in (%s))
        AND p.id = tm.photo_id
        GROUP BY p.id
        HAVING COUNT( t.id ) = %s) as tmp;"""

SELECT_QUERY = """
    SELECT p.src, p.created_at, p.likes,
        GROUP_CONCAT(t.name ORDER BY t.name SEPARATOR ', ') AS tags
    FROM tagmap tm, photo p, tag t
    WHERE tm.tag_id = t.id
    AND (t.name in (%s))
    AND t.off <> 1
    AND p.id = tm.photo_id
    GROUP BY p.id
    HAVING COUNT( t.id ) = %s
    %s
    LIMIT %s OFFSET %s;""" % ('%s', '%s', '%s', PER_PAGE, '%s')

# ORDER BY p.created_at DESC
TAGS_QUERY = "SELECT name FROM tag;"

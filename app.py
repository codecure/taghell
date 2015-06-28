# coding: utf-8
import time
import json
from flask import Flask, request, url_for, g, abort
from flask.ext.cache import Cache

from pagination import Pagination


cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
cache.init_app(app)
app.debug = True
pagination = Pagination()


@app.before_request
def before_request():
    g.request_start = time.time()
    g.request_time = lambda: '%.5fs' % (time.time() - g.request_start)


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
@cache.cached(timeout=50)
def photo_listing(page):
    tags = request.args.getlist('tag')
    sort = request.args.get('sort')
    sort_direction = request.args.get('sort_direction')
    pages = pagination.total_pages(tags)

    if page > pages or page < 1:
        abort(404)
    if sort not in [None, 'created_at', 'likes']:
        abort(404)
    if sort_direction not in [None, 'asc', 'desc']:
        abort(404)

    photos = pagination.get_photos(tags, page, sort, sort_direction)

    pagination_result = dict(
        items=[],
        has_prev=page > 1,
        has_next=page < pages,
        pages=pages,
        page=page,
    )

    for p in pagination.iter_pages(pages, page):
        url = url_for(
            'photo_listing', page=p, tag=tags,
            _external=True) if p != '...' else None
        pagination_result['items'].append(
            dict(page=p, url=url))

    result = dict(
        pagination=pagination_result,
        photos=photos,
        time=g.request_time()
    )

    return json.dumps(result)


@app.route('/tags')
@cache.cached(timeout=50)
def tags_list():
    return json.dumps([t[0] for t in pagination.tags_list()])


if __name__ == '__main__':
        app.run()

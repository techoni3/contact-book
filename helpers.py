from flask import abort

def get_paginated_list(results, url='/contact', start=1, limit=10):
    # check if page exists
    count = len(results)
    if (count < start):
        abort(404)
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj
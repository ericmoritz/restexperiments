from webob import Request


def never_cache(app):
    def inner(environ, start_response):
        req = Request(environ)
        resp = req.get_response(app)
        resp.cache_expires(0)
        return resp(environ, start_response)
    return inner


def cache_expires(seconds):
    def decor(app):
        def inner(environ, start_response):
            req = Request(environ)
            resp = req.get_response(app)
            resp.cache_expires(seconds)
            return resp(environ, start_response)
        return inner
    return decor

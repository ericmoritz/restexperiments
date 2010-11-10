from webob import exc


class FrontController(object):
    def __init__(self, **resource_map):
        self.resource_map = resource_map

    def __call__(self, environ, start_response):
        match = environ['wsgiorg.routing_args'][1]

        if match is None or "resource" not in match:
            return exc.HTTPNotFound()(environ, start_response)

        app = self.resource_map[match['resource']]
        return app(environ, start_response)


def serve(application):
    from paste.httpserver import serve
    serve(application, host="127.0.0.1",
          port=8000)

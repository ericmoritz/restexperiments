from webob import exc


class FrontController(object):
    def __init__(self, *resources):
        self.resources = resources

    def __call__(self, environ, start_response):
        # This selector is used to create a consistant
        # overhead for each resource
        apps = [a for prefix, a in self.resources
                   if environ.get('PATH_INFO', '').startswith(prefix)]

        if len(apps) == 0:
            msg = "%s %s" % (environ.get('SCRIPT_NAME',''), environ.get('PATH_INFO', ''), )
            msg +="\nTried %r" % [prefix for prefix, app in self.resources]

            return exc.HTTPNotFound(msg)(environ, start_response)            

        app = apps[0]
        script_name = environ.get('SCRIPT_NAME', '')
        environ['SCRIPT_NAME'] = script_name + prefix
        environ['PATH_INFO'] = environ.get('PATH_INFO', '')[len(prefix):]

        return app(environ, start_response)



def serve(application):
    #from paste.httpserver import serve
    #serve(application, host="127.0.0.1",
    #      port=8000)

    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, application)
    print "Serving on port 8000..."
    httpd.serve_forever()

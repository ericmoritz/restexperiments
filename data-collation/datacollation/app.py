from datetime import datetime
import time
import urllib
from webob import Response, Request
from httplib2 import Http

http_client = Http("/tmp/httplib2_cache")

def GET(uri):
    resp, content = http_client.request(uri, "GET")
    return content

def never_cache(app):
    def inner(environ, start_response):
        req = Request(environ)
        resp = req.get_response(app)
        resp.cache_expires(0)
        return resp(environ, start_response)
    return inner

###
## This provides the elements to collate the data
###

def get_data():
    """Returns two pieces of data that could be collated arbitrarily."""
    return {
        'children': ['Aiden Moritz', 'Ethan Moritz',],
        'spouse': 'Gina Moritz',
        }

def children(environ, start_response):
    """Provides RESTful access to the children data"""
    data = get_data()
    start_response("200 OK", [("Content-Type", "text/plain+csv")])
    return [",".join(data['children'])]

def spouse(environ, start_response):
    data = get_data()
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [data['spouse']]


####
## Collation solutions
####
def control(environ, start_response):
    """This is the control.  No access to data whatsoever but produces the
expected response."""
    start_response("200 OK", [("Content-Type", "text/plain")])
    return ["Gina Moritz;Aiden Moritz,Ethan Moritz"]

    
def direct_access(environ, start_response):
    data = get_data()
    start_response("200 OK", [("Content-Type", "text/plain")])
    spouse = data['spouse']
    children = ",".join(data['children'])

    return ["%s;%s" % (spouse, children)]


def indirect_access(environ, start_response):
    spouse = GET("http://localhost:8000/spouse")
    children= GET("http://localhost:8000/children")
    
    start_response("200 OK", [("Content-Type", "text/plain")])
    return ["%s;%s" % (spouse, children)]

def indirect_access_varnish(environ, start_response):
    spouse = GET("http://localhost:10001/spouse")
    children= GET("http://localhost:10001/children")
    
    start_response("200 OK", [("Content-Type", "text/plain")])
    return ["%s;%s" % (spouse, children)]


def esi_access(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    src = ("""<esi:include src="http://localhost:8000/spouse"/>;"""
           """<esi:include src="http://localhost:8000/children"/>""")
    return [src]


def ajax_html(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/html")])
    
    # This is some pseudo-code to mimic some code on-demand
    # that will collate the data client side
    src = """<script>
document.write(GET("http://localhost:10001/spouse"));
document.write(GET("http://localhost:10001/children"));</script>"""

    return [src]


class FrontController(object):
    def __init__(self, resource_map, debug=False):
        self.debug = debug
        self.resource_map = resource_map
        if "/" not in self.resource_map:
            self.resource_map['/'] = self.index

    def index(self, environ, start_response):
        req = Request(environ)

        urls = [req.host_url + req.relative_url(uri)
                for uri in self.resource_map]
    
        start_response("200 OK", [("Content-Type", 'text/plain')])
        return ["\n".join(urls)]

    def __call__(self, environ, start_response):
        try:
            app = self.resource_map[environ['PATH_INFO']]
        except KeyError:
            start_response("404 Not Found", [])
            return []

        return app(environ, start_response)

        


application = FrontController({
        # collation resources
        '/control': control,
        '/direct': direct_access,
        '/indirect': indirect_access,
        '/esi': esi_access,

        # Client side collator
        '/ajax.html': ajax_html,

        # data resources
        '/spouse': spouse,
        '/children': children,

 })

# Make it so that varnish never caches any of the data collation responses
application = never_cache(application)

if __name__ == '__main__':
    from paste.httpserver import serve
    serve(application, host="127.0.0.1",
          use_threadpool=True,
          threadpool_workers=5,
          port=8000)

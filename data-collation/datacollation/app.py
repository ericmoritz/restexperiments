from datetime import datetime
import time
import urllib
from webob import Response, Request
import gevent
from gevent import monkey; monkey.patch_socket()

def GET(*uris):
    def co(uri):
        return urllib.urlopen(uri).read()

    jobs = [gevent.spawn(co, uri) for uri in uris]
    gevent.joinall(jobs, timeout=2)

    values = [j.value for j in jobs]
    if len(jobs) == 1:
        return values[0]
    else:
        return values

def never_cache(app):
    def inner(environ, start_response):
        req = Request(environ)
        resp = req.get_response(app)
        resp.expires = datetime.utcnow()
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
    spouse, children = GET("http://localhost:8000/spouse",
                           "http://localhost:8000/children")
    
    start_response("200 OK", [("Content-Type", "text/plain")])
    return ["%s;%s" % (spouse, children)]

def indirect_access_varnish(environ, start_response):
    spouse, children = GET("http://localhost:10001/spouse",
                           "http://localhost:10001/children")
    
    start_response("200 OK", [("Content-Type", "text/plain")])
    return ["%s;%s" % (spouse, children)]


def esi_access(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    src = ("""<esi:include src="http://localhost:8000/spouse"/>;"""
           """<esi:include src="http://localhost:8000/children"/>;""")
    return [src]


def application(environ, start_response):
    resource_map = {
        # collation resources
        '/control': control,
        '/direct': direct_access,
        '/indirect': indirect_access,
        '/indirect_varnish': indirect_access_varnish,
        '/esi': esi_access,

        # data resources
        '/spouse': spouse,
        '/children': children,
        }
    try:
        app = resource_map[environ['PATH_INFO']]
    except KeyError:
        start_response("404 Not Found", [])
        return []

    return never_cache(app)(environ, start_response)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, application)
    print "Serving on port 8000..."
    httpd.serve_forever()
    

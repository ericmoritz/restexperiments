from restexperiments.core import db
from restexperiments.core.client import GET
from webob import Request

def spouse(environ, start_response):
    spouse = environ['get_spouse']()
    start_response("200 OK", [("Content-Type", "text/plain")])

    return [spouse]


def children(environ, start_response):
    children = environ['get_children']()
    start_response("200 OK", [("Content-Type", "text/plain")])

    return [",".join(children)]


def render(spouse, children):
    return "%s;%s" % (spouse,
                      ",".join(children))


def direct_family(environ, start_response):
    spouse = environ['get_spouse']()
    children = environ['get_children']()

    start_response("200 OK", [("Content-Type", "text/plain")])
    return [render(spouse, children)]


def indirect_family(environ, start_response):
    req = Request(environ)

    spouse_uri = "http://localhost:8000/phase1/restful/spouse"
    children_uri = "http://localhost:8000/phase1/restful/children"

    spouse = GET(spouse_uri)
    children = GET(children_uri)
    start_response("200 OK", [("Content-Type", "text/plain")])
    return ["%s;%s" % (spouse, children)]


def esi_family(environ, start_response):
    req = Request(environ)

    spouse_uri = "http://localhost:8000/phase1/restful/spouse"
    children_uri = "http://localhost:8000/phase1/restful/children"


    start_response("200 OK", [("Content-Type", "text/plain")])
    return ['<esi:include src="%s" />;<esi:include src="%s" />' %\
        (spouse_uri, children_uri)]

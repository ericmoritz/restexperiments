from restexperiments.core import db
from restexperiments.core.client import GET


def spouse(environ, start_response):
    spouse = db.get_spouse()
    start_response("200 OK", [("Content-Type", "text/plain")])

    return [spouse]


def children(environ, start_response):
    children = db.get_spouse()
    start_response("200 OK", [("Content-Type", "text/plain")])

    return [",".join(children)]


def render(spouse, children):
    return "%s;%s" % (spouse,
                      ",".join(children))


def direct_family(environ, start_response):
    spouse = db.get_spouse()
    children = db.get_children()

    start_response("200 OK", [("Content-Type", "text/plain")])
    return [render(spouse, children)]


def indirect_family(environ, start_response):
    url = environ['routes.url']

    spouse = GET(url("spouse"))
    children = GET(url("children"))
    return [render(spouse, children)]


def esi_family(environ, start_response):
    url = environ['routes.url']

    spouse_uri = url("restful/spouse")
    children_uri = url("restful/children")

    return '<esi:include src="%s" />;<esi:include src="%s" />' %\
        (spouse_uri, children_uri)

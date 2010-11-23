from restexperiments.core.controllers import FrontController
from restexperiments.core.cache import never_cache
from restexperiments.core.client import GET


def control(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return ""


def spouse(environ, start_response):
    spouse = environ['get_spouse']()
    start_response("200 OK", [("Content-Type", "text/plain")])

    return [spouse]


def children(environ, start_response):
    children = environ['get_children']()
    start_response("200 OK", [("Content-Type", "text/plain")])

    return [",".join(children)]


def template(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return ["{{ spouse }};{{ children }}"]


def direct_family(environ, start_response):
    spouse = environ['get_spouse']()
    children = environ['get_children']()
    start_response("200 OK", [("Content-Type", "text/plain")])
    return ["%s;%s" % (spouse, children)]


def indirect_family(environ, start_response):
    spouse_uri = "http://localhost:8000/phase1/restful/spouse"
    children_uri = "http://localhost:8000/phase1/restful/children"

    spouse = GET(spouse_uri)
    children = GET(children_uri)
    start_response("200 OK", [("Content-Type", "text/plain")])
    return ["%s;%s" % (spouse, children)]

###
# Implementations
###
application = FrontController(
    ('/control', control),
    ('/spouse', spouse),
    ('/children', children),
    ('/template', template),
    ('/direct/family', direct_family),
    ('/indirect/family', indirect_family),
)

application = never_cache(application)

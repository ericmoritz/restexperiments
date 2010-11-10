from routes import Mapper
from restexperiments.core.controllers import FrontController
from routes.middleware import RoutesMiddleware
from apps import conventional, restful

mapper = Mapper()


def control(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return ["Gina Moritz;Aiden Moritz,Ethan Moritz"]

###
# Implementations
###
mapper.connect("control",
               "/control",
               resource="control")

mapper.connect("conventional/direct/family",
               "/conventional/direct/family",
               resource="conventional/direct/family")

mapper.connect("restful/direct/family",
               "/restful/direct/family",
               resource="restful/direct/family")

mapper.connect("restful/indirect/family",
               "/restful/indirect/family",
               resource="restful/indirect/family")

mapper.connect("restful/esi/family",
               "/restful/esi/family",
               resource="restful/indirect/family")

mapper.connect("restful/spouse",
               "/restful/spouse",
               resource="restful/spouse")

mapper.connect("restful/children",
               "/restful/children",
               resource="restful/children")


application = FrontController(**{
        'control': control,
        'conventional/direct/family': conventional.direct_family,
        'restful/direct/family': restful.direct_family,
        'restful/indirect/family': restful.indirect_family,
        'restful/esi/family': restful.esi_family,
        'restful/spouse': restful.spouse,
        'restful/children': restful.children,
})

application = RoutesMiddleware(application, mapper)

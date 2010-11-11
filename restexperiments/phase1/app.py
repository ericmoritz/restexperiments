from restexperiments.core.controllers import FrontController
from restexperiments.core.cache import never_cache
from apps import conventional, restful


def control(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return ["Gina Moritz;Aiden Moritz,Ethan Moritz"]

###
# Implementations
###
application = FrontController(
    ('/control', control),
    ('/restful/spouse', restful.spouse),
    ('/restful/children', restful.children),
    ('/conventional/direct/family', conventional.direct_family),
    ('/restful/direct/family', restful.direct_family),
    ('/restful/indirect/family', restful.indirect_family),
    ('/restful/esi/family', restful.esi_family),
)

application = never_cache(application)

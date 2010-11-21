from restexperiments.core.controllers import FrontController
from restexperiments.core.cache import cache_expires
from apps import conventional, restful

# The control is the best technique from phase2 to provide a baseline
# of what an resources without caching looks like
from restexperiments.phase1.apps.conventional import direct_family as control

###
# Implementations
###
application = FrontController(
    ('/control', control),
    ('/conventional/memcache,direct/family', conventional.memcache_family),
    ('/restful/spouse', cache_expires(30)(restful.spouse)),
    ('/restful/children', cache_expires(30)(restful.children)),
    ('/restful/ajax/family', cache_expires(30)(restful.esi_family)),
    ('/restful/http,direct/family', cache_expires(30)(restful.direct_family)),
    ('/restful/http,esi/family', cache_expires(30)(restful.esi_family)),
)

application = application

from core.controllers import FrontController, serve
from routes import Mapper
from routes.middleware import RoutesMiddleware
from phase1.app import application as phase1

mapper = Mapper()
mapper.connect("phase1", "/phase1{path_info:.*}",
               resource="phase1")

application = FrontController(phase1=phase1)
application = RoutesMiddleware(application, mapper)

if __name__ == '__main__':
    serve(application)

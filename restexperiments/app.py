from core.controllers import FrontController, serve
from phase1.app import application as phase1

application = FrontController(
    ("/phase1", phase1),
)

if __name__ == '__main__':
    serve(application)

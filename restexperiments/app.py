from core.controllers import FrontController, serve
from core import db
from phase1.app import application as base_app
import time


def add_latency(secs):
    def decor(func):
        def inner(*args, **kwargs):
            time.sleep(secs)
            return func(*args, **kwargs)
        return inner
    return decor

# This middleware adds latency to the database calls
class LatencyConfigMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['get_spouse'] = add_latency(0.01)(db.get_spouse)
        environ['get_children'] = add_latency(0.01)(db.get_children)
    
        return self.app(environ, start_response)

# This middleware allows the database calls to be referenced in the
# WSGI environment
class ConfigMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['get_spouse'] = db.get_spouse
        environ['get_children'] = db.get_children

        return self.app(environ, start_response)

phase1 = ConfigMiddleware(base_app)
phase2 = LatencyConfigMiddleware(base_app)

application = FrontController(
    ("/phase1", phase1),
    ("/phase2", phase2),
)

if __name__ == '__main__':
    serve(application)

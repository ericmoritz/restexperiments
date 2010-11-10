from restexperiments.core import db


def direct_family(environ, start_response):
    spouse = db.get_spouse()
    children = db.get_children()

    start_response("200 OK", [("Content-Type", "text/plain")])
    return "%s;%s" % (spouse, 
                      ",".join(children))



def direct_family(environ, start_response):
    spouse = environ['get_spouse']()
    children = environ['get_children']()

    start_response("200 OK", [("Content-Type", "text/plain")])
    return "%s;%s" % (spouse, 
                      ",".join(children))


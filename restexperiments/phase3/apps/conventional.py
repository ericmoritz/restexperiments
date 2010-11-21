

def memcache_family(environ, start_response):
    # Here we get the current configuration from the WSGI environment
    cache = environ['memcache_client']
    get_spouse = environ['get_spouse']
    get_children = environ['get_children']
    #
    # Fetch Data
    # -----------
    #
    # Here we fetch the spouse from the cache
    spouse = cache.get("spouse")
    # If the spouse was not in the cache already, we get the spouse from the
    # database  and update the cache
    if spouse is None:
        spouse = get_spouse()
        cache.set("spouse", spouse, 30)
    #
    # Here we fetch the children from the cache
    children = cache.get("spouse")
    # If the children is not in the cache already, we get the children from the
    # database and update the cache
    if children is None:
        children = get_children()
        cache.set("children", children, 30)
    #
    # Generate Response
    # -------------------
    #
    start_response("200 OK", [("Content-Type", "text/plain")])
    return "%s;%s" % (spouse,
                      ",".join(children))

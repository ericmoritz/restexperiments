Caching
===============

Web developers are well aware that caching will the increase
performance of your web application.  This experiment will examine
traditional methods of internal caching versus RESTful HTTP/1.1 caching.

This experiment will focus on expiration based caching, conditional
HTTP caching will be addressed in a separate test.

Solutions
----------
Traditional web developers focus primarily on internal data caching
where as RESTful HTTP/1.1 caching focuses on passing the
responsibility of caching to an external caching proxy.

Internal Data Caching
~~~~~~~~~~~~~~~~~~~~~~

Internal data caching focuses on caching the actual data that is used
to generate an output.  The process of cache validation is as
follows::

    if key not in cache:
        data = get_current_data()
        cache.set(key, data, expiration)
    else:
        data = cache.get(key)
    return data
    
HTTP/1.1 caching
~~~~~~~~~~~~~~~~~
HTTP/1.1 caching is accomplished by setting the Expires HTTP header.
It is then the responsibility of an intermediary to cache the
response.


Hypothesis
-----------

External HTTP/1.1 caching will be faster because the application layer
is never contacted when the response is cached.


Test Cases
-----------

control
    Response is hard-coded to produce a baseline

simplecache
    werkzeug.contrib.cache.SimpleCache is used to accomplish internal
    data caching using an in-process memory cache

memcached
    python-memcache is used to accomplish internal data caching using a
    memcache server

libmc
    pylibmc is used to accomplish internal data caching
    using a memcached server using libmemcached.  This case is here to
    provide completeness for memcached solutions. libmc appears to be
    the most popular libmemcached solution.

middleware
    A WSGI middleware is used with HTTP/1.1 caching to provide
    in-application HTTP/1.1 caching

varnish
    Varnish is used to provide external HTTP/1.1 caching

Methodology
------------


Results
--------

[Present analyzed data]

Conclusion
-----------

[Present you conclusion]

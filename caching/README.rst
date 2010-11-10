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

    data = cache.get(key)
    if data is None:
        data = get_data()
	cache.set(key, data, seconds)
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
The tests are based on the data-collate example.  The WSGI applications
will produces the following response::

    Gina Moritz;Aiden Moritz,Ethan Moritz

For this experiment the WSGI applications will be working with cached
data instead of live content.  

The internal caching methods will get the spouse and children data
from the cache individually to simulate the process a web develop
would go through to retrieve two pieces of data from a cache

The HTTP/1.1 tests will fetch the two piece of data through URIs
that have the appropriate expiration headers set.

Cases
~~~~~~
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
    A WSGI app will fetch two resources who have been cached using
    HTTP/1.1 by the means of internal caching 

varnish_indirect
    A WSGI app will fetch two resources who have been cached using
    HTTP/1.1 via Varnish

esi
    A WSGI app provides a ESI template that Varnish uses to collate
    two HTTP cached resources

Methodology
------------


Results
--------

[Present analyzed data]

Conclusion
-----------

[Present you conclusion]

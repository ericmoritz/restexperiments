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

External HTTP/1.1 Using ESI will be faster because it excludes
the application server for cached content


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

Starting with a new Ubuntu 10.10 Rackspace Cloud 256 VPS.  Did the
following::

    git clone git://github.com/ericmoritz/restexperiments.git
    cd restexperiments
    ./ubuntu-10-10-build.sh
    ./start_varnish.sh & # wait a second for it to come up
    cd caching
    ./test.sh
    cp result/*.txt data/

The test.sh script runs the following command for each 
test case::

    ab -n 10000 -c1 {Case URI}


Results
--------

================= ==================== ====================
Case               Requests per second            ± control
================= ==================== ====================
control                        1322.38                 0.00
esi                             635.09               687.29
libmc                           549.96               772.42
memcache                        518.60               803.78
middleware                      509.70               812.68
simple                          507.27               815.11
varnish_indirect                396.42               925.96
================= ==================== ====================

================= ===================== =====================
Case               Time(ms) per request             ± control
================= ===================== =====================
control                           0.756                 0.000
esi                               1.575                -0.819
libmc                             1.818                -1.062
memcache                          1.928                -1.172
middleware                        1.962                -1.206
simple                            1.971                -1.215
varnish_indirect                  2.523                -1.767
================= ===================== =====================

Conclusion
-----------

The ESI test case did indeed beat the other tests. The difference
between the RESTful ESI solution and the traditional memcache solution
is quite negligable.  I am still quite disapointed by the indirect
performance.  I'd like to investigate that further to see what is
causing the overhead.



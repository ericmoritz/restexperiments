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

Serve Side Collation/Caching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These are the numbers for cases that are collated on the
server

================= ==================== ====================
Case               Requests per second            ± control
================= ==================== ====================
control                        1314.49                 0.00
esi                             634.87               679.62
middleware                      523.15               791.34
varnish_indirect                506.06               808.43
libmc                           455.98               858.51
memcache                        439.60               874.89
simple                          426.61               887.88
================= ==================== ====================

================= ===================== =====================
Case               Time(ms) per request             ± control
================= ===================== =====================
control                           0.761                 0.000
esi                               1.575                -0.814
middleware                        1.912                -1.151
varnish_indirect                  1.976                -1.215
libmc                             2.193                -1.432
memcache                          2.275                -1.514
simple                            2.344                -1.583
================= ===================== =====================

Client-Side Collating
~~~~~~~~~~~~~~~~~~~~~~

This is the result of Client-Side Collating of the resources.
There are three resources requested. /spouse, /children, and
/ajax.html to mimic the number of requests needed to collate
the two resources.  The /ajax.html response is simply some
pseudocode that resembles the code needed to collate the 
/spouse and /children resources.

It is hard to come up with accurate numbers due to the unknown
overhead that would be introduced by the processing the 
ajax.html file.  An additional unknown is the benefit of
the ability of browsers to fetch resources asyncronously.

I am going to fudge things and assume that the benefit
of async fetching and the overhead of processing cancel 
each other out.  To calculate the mean time per request
I will sum the total time for each tests and divide by
the sample size.

================= =====================
Case               Time(ms) per request
================= =====================
ajax                              0.626
esi                               1.575


Conclusion
-----------

The ESI test case did indeed beat the other tests. The difference
between the RESTful ESI solution and the traditional memcache solution
is quite negligable.  I am still quite disapointed by the indirect
performance.  I'd like to investigate that further to see what is
causing the overhead.

When considering ESI versus client-side collating of cached data.
It appears that fetching three cached resources is faster than
fetching one uncached ESI collated resource that was built using
cached resources

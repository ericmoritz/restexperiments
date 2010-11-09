Comparison of Caching methods
==============================

This is an experiment to demonstrate how using HTTP/1.1 caching and a
caching proxy server fair exceeds the capabilities of caching inside
the application layer.


Hypothesis
-----------

External HTTP/1.1 caching will out perform caching within the
application layer

Methodology
------------

I created a new Ubuntu 10.10 256MB server on `rackspacecloud`_. I
configured the server by running the following commands::

    apt-get update
    apt-get install git varnish python-setuptools memcached apache2-utils
    git clone git://github.com/ericmoritz/experiments.git
    cd experiments/cachecompare
    python setup.py develop
    python cachecompare/tests/test.py &> /dev/null

.. _rackspacecloud: http://www.rackspacecloud.com/cloud_hosting_products/servers/pricing

The test.py script did the following for each test case.

#. Spawned a wsgiref HTTP server for the WSGI application implementing a
   cache technique.
#. Primed the cache by prefetching the URI being tested. The results are
   stored at results/<case>.html to confirm the WSGI application is
   functioning properly.
#. Ran Apache Bench configured to make 1000 requests in a single thread
#. Dumped the results of apache bench to restuls/<case>.ab.txt


Test Cases
-----------
Each test case was based on the `so-starving`_ Django application.
There were two variables in the basic test that needed to be
eliminated.

.. _so-starving: https://github.com/agiliq/so-starving

The first variable was the Facebook search URI.  I hard-coded the data
from a request to that URI to eliminate the varience introduced by
Facebook's API.

The second variable was json parsing.  I eliminated the need to parse
the JSON data because once the data was hard-coded, it no longer
needed to be parsed.

The test.py script did the following for each test case.

#. Spawned a wsgiref HTTP server for the WSGI application implementing
   a cache technique.
#. Primed the cache by prefetching the URI being tested.  The results
   are stored at results/<test case>.html to confirm the WSGI
   application is functioning properly.
#. Ran Apache Bench configured to make 1000 requests in a single
   thread
#. Dumped the results of apache bench to restuls/<test case>.ab.txt

Cases
~~~~~~

control
   This application simply renders the data with a template

locmem
   This uses django.core.cache with the locmem backend to do
   application level caching of data.  The view checks the existence
   of the data in the cache and if it exists it will render that data
   using a template.

memcache
   This uses django.core.cache with the memcache backend to do
   application level caching of data.  The view checks the existence
   of the data in the cache and if it exists it will render that data
   using a template.

middleware
   This uses the django.middleware.cache middleware to handle HTTP/1.1
   caching inside the application layer.  The view sets the Expires
   header and the middleware uses locmem to cache the response body.

varnish
   This uses Varnish to provide an external HTTP/1.1 cache. The
   view sets the Expires header and Varnish is used to cache
   the response body.


Results
--------

Mean requests per second
~~~~~~~~~~~~~~~~~~~~~~~~~

============== =============================
Case            Requests per second          
============== =============================
varnish                              5043.22
middleware                            741.43
control                               484.01
locmem                                403.02
memcache                              358.21
============== =============================

Conclusion
-----------

It is quite obvious to see why an external
HTTP/1.1 caching server would increase the number of requests per
second.  The external server eliminates the need for the application
to validate the cache.

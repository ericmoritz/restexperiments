Phase 3
===============

Everyone in the world just has to read about my family; So now my
database is overloaded and I'm seeing query times around 10ms. My
concurrency levels and I have done everything in my power to optimize
my queries, now what?

Since hopefully my children and spouse resources will not be changing
anytime soon, I can add expiration based caching onto the resources.

Solutions
----------

Conventional Design
~~~~~~~~~~~~~~~~~~~~

The traditional design is do ad-hoc caching with a cache back-end.
The most popular way of doing this is to use memcached and to talk to
it directly.  The conventional way of doing that is as follows::

    data = cache.get("somekey")
    if data is None:
        data = get_data()
        # Cache for 30 seconds
        cache.set("somekey", data, 30)

    return data


RESTful Design
~~~~~~~~~~~~~~~

While a RESTful resource could very well use memcached directly, the
process would be the same as the conventional method.  There is no
need for us to test that technique with the RESTful /family resource.

Something that we can take advantage with RESTful resources is HTTP
caching.

Direct Access
^^^^^^^^^^^^^^^

We will use the HTTP Expires header to add caching to the RESTful 
/direct/family resource.

ESI
^^^^

We will use the ESI template from previous examples but the 
/esi/family and /spouse and /children resources will all have Expires
headers to add HTTP caching.


Hypothesis
-----------

I believe that talking to memcached direct will be faster than using
HTTP caching because direct access in previous tests proved to be the fastest.


Test Cases
-----------

/control
   The control will be the /conventional/direct/family resource from
   phase2.  I chose this because it performed the best for a technique
   that had no caching.

/conventional/memcache,direct/family
   We will use the direct method from previous tests and use memcached
   to fetch cached data

/restful/http,direct/family
   We will use the direct method from previous tests but use the HTTP
   Expires header to cache the response.

/restful/http,esi/family
   We will use the ESI method from previous tests but the spouse,
   children and ESI templates will haave Expires headers


Methodology
------------

I will run the tests in the same methodology as phase1 but using the
URIs for this test.

Results
--------


.. raw:: html

  <script
    src="_static/highcharts.js"
    type="text/javascript"></script>
  <script
    src="_static/csvchart.js"
    type="text/javascript"></script>
  <script
    src="_static/phase3.js"
    type="text/javascript"></script>


  <div id="phase3-rps-chart"></div>

  <div id="phase3-tpr-chart"></div>


Conclusion
-----------

I am seeing unexpected results for the 1 concurrent user test run.  I
am going to suspend my conclusion until I verify that everything is
correct with the test harness.

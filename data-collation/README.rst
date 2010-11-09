Data Collation
===============

Data Collation is a very common need in a web application.  A front
page of a website could be a combination of a number of pieces of
data.

A RESTful web application provides data as a set of resources
identified by URIs.  Collation of data in a RESTful web application
can be accomplished in a couple of ways:

* Edge Side Includes
* Client Side AJAX
* Internal collation with indirect access to data via resources
* Internal collation with direct access to data

Tradition web applications collate data in one way:

* Internal collation with direct access to data

Hypothesis
-----------
Internal collation with direct access to data will be faster than
other methods

Methodology
------------

I started varnish using the ../start_varnish.sh script.  In order to
accomplish the indirect test case I needed a multiprocess server.  I
used gunicorn with the following command line::

    cd datacollation
    gunicorn -w 3 app

I then ran *test.sh* which test each case using ab with the following
command line::

    ab -n 10000 -c 1 $URI

Test Cases
-----------

control
    Hard coded the response to create a baseline to compare the
    overhead of the individual techniques

direct
    Uses a dictionary and string formatting to combine the two pieces
    of data

indirect
    Uses urllib to fetch the two pieces of data by the means of
    web resources identified by URIs

esi
    Uses Varnish's ESI functionality to fetch the two pieces of data
    by means of web resources identified by URIs


Results
--------
============== =============================
Case            Requests per second          
============== =============================
control                              1718.27
direct                               1686.63
esi                                  1150.59
indirect                              274.19
============== =============================

============== ==============================
Case            Time(ms) per request          
============== ==============================
control                                 0.582
direct                                  0.593
esi                                     0.869
indirect                                3.647
============== ==============================


Conclusion
-----------

There is no question that direct access to the data would produce a
the fastest result.  It is the test case with the least number of
moving parts.

It was quite surprising that the indirect method performed so poorly
but ESI performed favorably.

In reality, the overhead in all solutions are in microsecond
resolutions which is pretty damn fast.  I would be comfortable using
any of these methods.

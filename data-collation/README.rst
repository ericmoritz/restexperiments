Data Collation
===============

Data Collation is a very common need in a web application.  A front
page of a website could be a combination of a number of pieces of
data.

Solutions
----------

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


Test Cases
-----------
Each test case is accomplished using a separate WSGI application
mounted at a URI of it's name.  Each application is responsible for
taking two pieces of data, "spouse" and "children" which correspond to
the relationships in my immediate family.  In essence they're
representing my close relations.

The response of each should produce the following output::

    Gina Moritz;Aiden Moritz,Ethan Moritz

We are working with simple string formatting here to eliminate
variables introduced by template engines.

Cases
~~~~~~~~~~~~

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

Results
--------

============== =============================
Case            Requests per second          
============== =============================
control                               871.72
direct                                864.28
esi                                   201.15
indirect                              157.14
============== =============================

============== ==============================
Case            Time(ms) per request          
============== ==============================
control                                 1.147
direct                                  1.157
esi                                     4.971
indirect                                6.364
============== ==============================

Conclusion
-----------

There is no question that direct access to the data would produce a
the fastest result. It is the test case with the least number of
moving parts.


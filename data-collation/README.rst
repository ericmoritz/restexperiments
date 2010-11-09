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

============== =============================
Case            Requests per second          
============== =============================
control                              1438.96
direct                               1232.23
esi                                   846.13
indirect                              167.89
============== =============================

Conclusion
-----------
My Hypothesis proved to be correct.  It's quite obvious that collating
data internally proves to be the fastest method; it is the method with
the least overhead.

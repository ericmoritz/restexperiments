REST vs. The World
===================

Modern web applications have a number of requirements that both
developers need and users need.  These experiments will compare
solutions presented by REST proponents versus current solutions.

Whenever the status quo is challenged, the burden of proof is on the
challenger.

Each solution presented effects the entire system.  I will start with
small tests and create new tests based of the results

Phase One
---------
At the very least, a web application is a data collator.  The data
collated may have varying degrees of latency.  When fetch a certain
piece of information results in an unacceptable latency, web
developers rely on caching to decrease tho wait on the user.

I will start with data collation first and base caching experiments
and the collation tests.

Data Collation
~~~~~~~~~~~~~~~

Traditional methods of collating data is accomplished through direct
access to the data.  The response of an URI may fetch some data from a
database, some other data from a file, etc.  Generally the data is
accessed directly.

Within a RESTful web application, there is the potential to access
data indirectly using URIs for Resources.  The data collation
experiment will explore which of these techniques are the fastest

* `Collation Results`_

.. _Collation Results: https://github.com/ericmoritz/restexperiments/tree/master/data-collation/README.rst


Caching
~~~~~~~~

The favored method of caching is accomplished by caching data
structured from within the application.  

RESTful caching favors HTTP/1.1 caching utilizing external cache
proxies and/or relying on client caching.

This experiment expands on the data collation experiment and adds
caching to the individual items.

The RESTful resources are cached using HTTP caching and the
alternatives use internal data caching


* `Caching Results`_

.. _Caching Results: https://github.com/ericmoritz/restexperiments/tree/master/caching/README.rst


